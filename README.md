![American University Of Cairo To Participate In 7th Gulf Education
\...](media/image1.png){width="3.591666666666667in"
height="2.7083333333333335in"}

**Embedded Systems**

**Project Report**

**Mohamed A. Abdel Hamed**

**900163202**

**Dr. Mohamed Shalan**

**Spring 2020**

**Overview & Description**

Presented is a real-time embedded ECG heart monitor system application.
The embedded side is to operate on an STM32F1 microcontroller (e.g.
Black Pill) while the desktop-side is to run on any Python3- supporting
environment. The ECG sensor being used is the SparkFun AD8232. The
application provides the two basic functionalities of a heart monitor,
namely, heart activity plotting, and heart beat rate reporting.
Furthermore, the app enables the user to control some side features such
as sampling and baud rates in addition to the COM port used. The
application also provides a graphical control panel for these features.

**This report is dedicated to discussing the following:**

I.  **Development Environment & Technology**

II. **System Features**

III. **Design & Implementation**

IV. **User Guide & Sample Runs**

V.  **Future Development**

```{=html}
<!-- -->
```
I.  **Development Environment & Technology**

**Software**

**Programming languages used**:

-   **Black Pill app:** developed in C

-   **PC app:** developed using Python 3.8.2

**Development software used:**

-   **Black Pill app: Keil uVision IDE + CubeMX**

-   **PC app:**

    -   **pySerial:** used for microcontroller-to-PC communication over
        a serial USB COM port

    -   **matplotlib:** used for real-time plotting

    -   **GUI:** used for graphical interface

**Hardware**

-   **Microcontroller:** STM32F1 Black Pill

-   **ECG Sensor:** SparkFun AD8232

-   ![](media/image2.png){width="2.28125in"
    height="1.7291666666666667in"}![](media/image3.jpeg){width="1.69375in"
    height="1.9715277777777778in"}![](media/image4.jpeg){width="2.101923665791776in"
    height="1.4012828083989501in"}**Serial Cable**: prolific USB-UART
    cable

II. **System Features**

**Functional Features:**

1.  **Serial Port Selection:** in the beginning, the user is prompted
    with the available COM ports for them to select the one, to which
    the microcontroller is hooked.

2.  **Baud Rate Control:** along with the port, the user is also
    prompted to set the desired baud rate (115200 is recommended).

3.  **Sampling Rate Control:** at any point during operation (except for
    when ECG data collection is ongoing), a user can set the desired
    sampling rate to be used for collecting heart activity data.

4.  **Collect & Plot ECG Data for 1 Minute:** a user can start the
    one-minute ECG data collection mode where the plot window is
    launched and updated real-time. Meanwhile, any other interaction is
    frozen until the plot window is closed.

5.  **Report Heart Beat Rate:** after at least one data collection run,
    the application can report the average HBR based on the collected
    data.

**Non-functional Features:**

1.  **Leads-off Detection:** the system detects if the sensor pads were
    not attached properly at some point and produces a flat middle line
    in the plot.

2.  **Premature Data Collection Cancelling:** in case the user closes
    the plot window midway through an ongoing data transmission, the
    desktop app signals the microcontroller to halt the data
    transmission from its side.

```{=html}
<!-- -->
```
III. **Design & Implementation**

**Low-level utilities:**

I.  **Command Extraction:** all commands read from the serial port byte
    by byte, and are delimited by '\$' as shown below:

![](media/image5.png){width="4.475in" height="0.9952887139107611in"}

![](media/image6.png){width="4.4in" height="2.090177165354331in"}

II. **Command Parsing:** once a command has been extracted, it is then
    passed for parsing it by its predefined handle (e.g. SSR), and then
    the corresponding procedure is selected based on that:

![](media/image7.png){width="4.730435258092738in"
height="2.794828302712161in"}

**In the following two sub-section, the implementation of each of the
aforementioned System Features are to be discussed.**

**Functional Features:**

i.  **Serial Port Selection:**

This is readily achieved through the pySerial utility tools as shown
below:

![](media/image8.png){width="6.5in" height="0.4736111111111111in"}

Note that it takes some time initially to detect the available ports
(\~5 seconds)

ii. **Baud Rate Control:**

> This is specified when the serial port is opened initially:

![](media/image9.png){width="6.5in" height="0.5159722222222223in"}

iii. **Sampling Rate Control:**

Sampling rate controlled through the period of GPTIM2 which triggers the
ADC1 conversions with each elapsed period when uC is in data collection
mode.

![](media/image10.png){width="6.5in" height="3.027083333333333in"}

When a user sets the heart beat rate through the control panel, a
formatted command is sent to the microcontroller (via UART), which gets
parsed and the auto-reload register (ARR) of the GPTIM2 is adjusted
according to the following formula:

-   ARR = $\frac{1000}{X} - 1;where\ X = desired\ sampling\ rate$

Given that the GPTIM2 source clock is 8 MHz, and the prescaler is fixed
at (8K -- 1), so the timer trigger rate becomes equivalent to the
sampling rate. The allowed range for the sampling rate is between 1 and
1000.

iv. **Collect & Plot ECG Data for 1 Minute:**

When this mode is triggered by the user, the microcontroller stops
waiting for new commands and keeps sending numerical data representing
the pulse magnitude relative to the ADC range (12 bits = 0 to 4095).
Every data reading is sent in a new line as shown:

![](media/image11.png){width="6.5in" height="0.47152777777777777in"}

When the uC is done sending data, it sends a pre-set ACK msg to signal
the desktop app to stop updating the plot.

![](media/image12.png){width="2.5833333333333335in"
height="0.3020833333333333in"}

![](media/image13.png){width="6.5in" height="0.7909722222222222in"}

The real-time plot update is done by periodically redrawing the plot to
reflect any new changes. In this app, the plot is refreshed every 10 ms:

![](media/image14.png){width="6.5in" height="0.25555555555555554in"}

So that achieves a refresh rate of around 100 fps. It is advised to
reduce that rate for devices (PCs) that cannot support that refresh
rate.

v.  **Report Heart Beat Rate:**

This is done by counting the beats detected during a 1-minute data
collection. A beat is defined as a pulse that's at least \~60% of the
ADC scale in magnitude. Due to limitations on the operation guarantees
at the user side, the heart beats counter is reset before each data
collection to prevent previous poorly operated (e.g. disconnected pads)
runs from corrupting the HBR.

**Non-functional Features:**

i.  **Leads-off Detection:** this is done by digitally reading the GPIO
    pin value of the LO+ & LO- sensor signals, and if they're high, the
    microcontroller sends a special pre-set character '!' to signal the
    PC app to flatten the plot at that point.

![](media/image15.png){width="5.25in" height="1.78125in"}

ii. **Premature Data Collection Cancelling:** this is achieved by
    sending a pre-agreed character '\#' to the uC to signal it to stop.

```{=html}
<!-- -->
```
IV. **User Guide & Sample Runs**

This guide assumes the user has the hardware described before (along
with a means to download the hex code to the uC) in addition to the
required software (including the Python packages).

-   Below are the steps to use the system:

    i.  Make sure all connections are as shown below.

    ii. Download the hex code to the Black Pill uC (e.g. though serial
        programming)

    iii. Put the uC into operation mode (if you're using SP) and click
         the Reset button.

    iv. Go to the "**main\_app**" directory and run the following
        command "**python** **main.py**"

![](media/image16.jpg){width="4.686956474190726in"
height="1.4229166666666666in"}

![](media/image17.png){width="5.426972878390202in"
height="1.86956583552056in"}

**Sample Run:**

V.  **Future Development & Improvement**

The following could be a potential improvement on the presented system:

1.  Using DMA for managing ADC conversions instead of interrupts

2.  Utilizing the SDN (shut down) signal of the AD8232 sensor to save
    power when we're not sampling its output.

3.  Using a smoother technique for updating graph data in real-time

4.  Adding a layer of fault tolerance around port binding in case of
    failures to connect to UART.

**References**

-   **AD8232 Sensor Datasheet**

-   **STM32F1 Datasheet**

-   [**https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time**](https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time)

-   [**https://pythonhosted.org/pyserial/index.html**](https://pythonhosted.org/pyserial/index.html)
