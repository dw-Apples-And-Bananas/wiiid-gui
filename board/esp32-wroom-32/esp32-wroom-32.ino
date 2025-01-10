#include "ESP32Wiimote.h"

ESP32Wiimote wiimote;

static bool logging = true;
static long last_ms = 0;
static int num_run = 0, num_updates = 0;

void setup()
{

    Serial.begin(115200);
    Serial.println("ESP32Wiimote");

    wiimote.init();
    if (! logging)
        wiimote.addFilter(ACTION_IGNORE, FILTER_ACCEL); // optional
    
    Serial.println("Started");
    last_ms = millis();
}

void loop()
{
    wiimote.task();
    num_run++;

    if (wiimote.available() > 0) 
    {
        ButtonState  button  = wiimote.getButtonState();
        AccelState   accel   = wiimote.getAccelState();
        NunchukState nunchuk = wiimote.getNunchukState();

        num_updates++;
        if (logging)
        {
            int ia     = (button & BUTTON_A)     ? 1 : 0;
            int ib     = (button & BUTTON_B)     ? 1 : 0;
            // int cc     = (button & BUTTON_C)     ? 'C' : '.';
            // int cz     = (button & BUTTON_Z)     ? 'Z' : '.';
            int i1     = (button & BUTTON_ONE)   ? 1 : 0;
            int i2     = (button & BUTTON_TWO)   ? 1 : 0;
            int iminus = (button & BUTTON_MINUS) ? 1 : 0;
            int iplus  = (button & BUTTON_PLUS)  ? 1 : 0;
            int ihome  = (button & BUTTON_HOME)  ? 1 : 0;
            int ileft  = (button & BUTTON_LEFT)  ? 1 : 0;
            int iright = (button & BUTTON_RIGHT) ? 1 : 0;
            int iup    = (button & BUTTON_UP)    ? 1 : 0;
            int idown  = (button & BUTTON_DOWN)  ? 1 : 0;
      
            // Serial.printf("button: %05x = ", (int)button);
            // Serial.print(ca);
            // Serial.print(cb);
            // Serial.print(cc);
            // Serial.print(cz);
            // Serial.print(c1);
            // Serial.print(c2);
            // Serial.print(cminus);
            // Serial.print(chome);
            // Serial.print(cplus);
            // Serial.print(cleft);
            // Serial.print(cright);
            // Serial.print(cup);
            // Serial.print(cdown);
            // Serial.printf(", wiimote.axis: %3d/%3d/%3d", accel.xAxis, accel.yAxis, accel.zAxis);
            // Serial.printf(", nunchuk.axis: %3d/%3d/%3d", nunchuk.xAxis, nunchuk.yAxis, nunchuk.zAxis);
            // Serial.printf(", nunchuk.stick: %3d/%3d\n", nunchuk.xStick, nunchuk.yStick);

            Serial.printf("r{\"a\":%d,\"b\":%d,\"1\":%d,\"2\":%d,\"-\":%d,\"+\":%d,\"h\":%d,\"<\":%d,\">\":%d,\"^\":%d,\"v\":%d}\n",
                                  ia,      ib,      i1,      i2,      iminus,  iplus,   ihome,   ileft,   iright,  iup,     idown);
              
            if (iright == 1) {
              wiimote.setLED(2);
            }
        }
    }

    if (! logging)
    {
        long ms = millis();
        if (ms - last_ms >= 1000)
        {
            Serial.printf("Run %d times per second with %d updates\n", num_run, num_updates);
            num_run = num_updates = 0;
            last_ms += 1000;
        }
    }

    delay(10);
}