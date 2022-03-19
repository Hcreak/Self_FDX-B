#include <WiFi.h>
#include <ESPmDNS.h>

const char *ssid = "ESPsoftAP_Test";
const char *password = "testtest";

WiFiServer server; //声明服务器对象

void setup()
{
    
    Serial.begin(9600);
    
    Serial.print("Setting soft-AP ... ");
    boolean result = WiFi.softAP(ssid, password);
    if(result == true)
    {
      Serial.println("Ready");
    }
    else
    {
      Serial.println("Failed!");
    }

    // Set up mDNS responder:
    // - first argument is the domain name, in this example
    //   the fully-qualified domain name is "esp32.local"
    // - second argument is the IP address to advertise
    //   we send our IP address on the WiFi network
    if (!MDNS.begin("fdx-b")) {
        Serial.println("Error setting up MDNS responder!");
        while(1) {
            delay(1000);
        }
    }
    Serial.println("mDNS responder started");

    // Start TCP server
    server.begin(7777); //服务器启动监听端口号22333
    Serial.println("TCP server started");

    // Add service to MDNS-SD
    MDNS.addService("fdx-b", "tcp", 7777);
}

void loop()
{
    
    WiFiClient client = server.available(); //尝试建立客户对象
    if (client) //如果当前客户可用
    {
    
        Serial.println("[Client connected]");
        String readBuff;
        while (client.connected()) //如果客户端处于连接状态
        {
    
            if (Serial.available() > 0)
            {
                String SerialData = Serial.readString();
                String CountryCode = SerialData.substring(1,5);
                String TagNumber = SerialData.substring(5,15);
                long int intCountryCode = strtol(CountryCode.c_str(), NULL, 16);
                // FUCK!!! LONG_MAX	 Maximum value for a variable of type long.	2147483647
                // Use strtoll, returns the converted integral number as a long long int value.
                // 8bit AVR not support long long int, 'strtoll' was not declared in this scope
                long long int intTagNumber = strtoll(TagNumber.c_str(), NULL, 16);

                // Serial.print("CountryCode: ");
                // Serial.println(CountryCode);
                // Serial.println(intCountryCode);
                // Serial.print("TagNumber: ");
                // Serial.println(TagNumber);
                // Serial.println(intTagNumber);

                char formatOut [16];
                sprintf (formatOut, "%04d%012lld", intCountryCode, intTagNumber);
                client.print(formatOut);
            }
        }
        client.stop(); //结束当前连接:
        Serial.println("[Client disconnected]");
    }
}
