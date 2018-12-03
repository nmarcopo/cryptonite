package com.example.cryptowatch;

import android.graphics.Color;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.wearable.activity.WearableActivity;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.style.ForegroundColorSpan;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;

import com.google.android.gms.common.util.IOUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.net.URL;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.HttpURLConnection;
import java.security.spec.ECField;
import java.text.DecimalFormat;
import java.util.Iterator;
import java.util.Scanner;

import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends WearableActivity {

    private TextView mTextView;
    private TextView value11;
    private TextView value22;
    private TextView value33;
    private TextView value44;
    private TextView value55;
    private Button hotButton;
    private Button coldButton;
    private String hottitle = "   HOT Cryptocurrencies\n";
    private String coldtitle = "  COLD Cryptocurrencies\n";
    private String myURL = "student04.cse.nd.edu:52109/crypto/";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Typeface typeface = Typeface.createFromAsset(getAssets(), "fonts/Consolas.ttf");
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        mTextView = (TextView) findViewById(R.id.mycrypto);
        value22 = findViewById(R.id.firstB);
        value33 = findViewById(R.id.secondB);
        value44 = findViewById(R.id.thirdB);
        value55 = findViewById(R.id.fourthB);
        value11 = findViewById(R.id.fifthB);

        value11.setTypeface(typeface);
        value22.setTypeface(typeface);
        value33.setTypeface(typeface);
        value44.setTypeface(typeface);
        value55.setTypeface(typeface);
        mTextView.setText("     Select HOT or COLD");

        hotButton = (Button) findViewById(R.id.HOT);
        coldButton = (Button) findViewById(R.id.COLD);

        hotButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                hotCrypto();
            }
        });
        coldButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                coldCrypto();
            }
        });

        // Enables Always-on
        setAmbientEnabled();
    }


    public void hotCrypto() {
        mTextView.setTextColor(Color.parseColor("#FFA500"));
       mTextView.setText(hottitle);
        value11.setText("");
        value22.setText("");
        value33.setText("");
        value44.setText("");
        value55.setText("");
        String Payload = "{'temp': 'hot', 'days': 10, 'count': 5, 'static': false}";
        new FetchDataHot().execute(Payload);
    }

    public void coldCrypto() {
        mTextView.setTextColor(Color.parseColor("#ADD8E6"));
        mTextView.setText(coldtitle);
        value11.setText("");
        value22.setText("");
        value33.setText("");
        value44.setText("");
        value55.setText("");
        String Payload = "{\"temp\": \"cold\", \"days\": 10, \"count\": 5, \"static\": false}";
        new FetchDataCold().execute(Payload);
    }

    public class FetchDataCold extends AsyncTask<String, Void, String> {


        @Override
        protected String doInBackground(String... params) {

            try {
                StringBuilder result = new StringBuilder();
                URL url = new URL("http://student04.cse.nd.edu:52109/crypto/cold");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String line;
                while ((line = rd.readLine()) != null) {
                    result.append(line);
                }
                rd.close();
                return result.toString();


            } catch (Exception e) {

            }
            return "hello";
        }

        protected void onPostExecute(String responseData) {
            Log.d("onpost", "RESPONSE DATA: " + responseData);
            JSONObject jsonO = null;
            try {
                jsonO = new JSONObject(responseData);
            } catch (Exception e) {

            }
            boolean val1;
            boolean val2;
            boolean val3;
            boolean val4;
            boolean val5;


            String key1;
            String value1;
            String key2;
            String value2;
            String key3;
            String value3;
            String key4;
            String value4;
            String key5;
            String value5;
            String tempString;
            String firstTemp;
            String secondTemp;
            String thirdTemp;
            String fourthTemp;
            String fifthTemp;
            String total;
            String price1;
            String price2;
            String price3;
            String price4;
            String price5;
            String coin1;
            String coin2;
            String coin3;
            String coin4;
            String coin5;

            Spannable spannable=null;
            Log.d("onpost", jsonO.toString());
            //for (int i = 0; i < jsonO.names().length()-1; i++) {
            try {
                Log.d("mytestparse",jsonO.getString("data"));
                String[] mykeys = jsonO.getString("data").split("\"");
                for(String key: mykeys)
                {
                    Log.d("mytestparse",key);

                }
                DecimalFormat df = new DecimalFormat("#0.00");
                Log.d("mynewparse",mykeys[1]);
                Log.d("mynewparse",mykeys[3]);
                Log.d("mynewparse",mykeys[5]);
                Log.d("mynewparse",mykeys[7]);
                Log.d("mynewparse",mykeys[9]);
                Log.d("mynewparse",mykeys[11]);
                Log.d("mynewparse",mykeys[13]);
                Log.d("mynewparse",mykeys[15]);
                Log.d("mynewparse",mykeys[17]);
                Log.d("mynewparse",mykeys[19]);
                Log.d("mynewparse",mykeys[4].substring(1,mykeys[4].length()-3));
                Log.d("mynewparse",mykeys[8].substring(1,mykeys[8].length()-3));
                Log.d("mynewparse",mykeys[12].substring(1,mykeys[12].length()-3));
                Log.d("mynewparse",mykeys[16].substring(1,mykeys[16].length()-3));
                Log.d("mynewparse",mykeys[20].substring(1,mykeys[20].length()-3));
                coin1= df.format(Float.parseFloat(mykeys[4].substring(1,mykeys[4].length()-3)));
                coin2= df.format(Float.parseFloat(mykeys[8].substring(1,mykeys[8].length()-3)));
                coin3= df.format(Float.parseFloat(mykeys[12].substring(1,mykeys[12].length()-3)));
                coin4= df.format(Float.parseFloat(mykeys[16].substring(1,mykeys[16].length()-3)));
                coin5= df.format(Float.parseFloat(mykeys[20].substring(1,mykeys[20].length()-3)));
                key1 = mykeys[1];
                value1 =mykeys[3];
                key2 = mykeys[5];
                value2 = mykeys[7];
                key3 = mykeys[9];
                value3 = mykeys[11];
                key4 = mykeys[13];
                value4 = mykeys[15];
                key5 = mykeys[17];
                value5 = mykeys[19];
                String formattedKey1 = String.format("%-5s",key1+":");
                String formattedKey2 = String.format("%-5s",key2+":");
                String formattedKey3 = String.format("%-5s",key3+":");
                String formattedKey4 = String.format("%-5s",key4+":");
                String formattedKey5 = String.format("%-5s",key5+":");

                DecimalFormat df2= new DecimalFormat("#00.00");
                String formattedvalue1 = df2.format(Float.parseFloat(value1.substring(0,value1.length()-1)));
                Log.d("mynewtestparse",formattedvalue1);
                String formattedvalue2 = df2.format(Float.parseFloat(value2.substring(0,value2.length()-1)));
                Log.d("mynewtestparse",formattedvalue2);
                String formattedvalue3 = df2.format(Float.parseFloat(value3.substring(0,value3.length()-1)));
                Log.d("mynewtestparse",formattedvalue3);
                String formattedvalue4 = df2.format(Float.parseFloat(value4.substring(0,value4.length()-1)));
                Log.d("mynewtestparse",formattedvalue4);
                String formattedvalue5 = df2.format(Float.parseFloat(value5.substring(0,value5.length()-1)));
                Log.d("mynewtestparse",formattedvalue5);
                if(formattedvalue1.startsWith("-"))
                    formattedvalue1=formattedvalue1.substring(1,formattedvalue1.length());
                if(formattedvalue2.startsWith("-"))
                    formattedvalue2=formattedvalue2.substring(1,formattedvalue2.length());
                if(formattedvalue3.startsWith("-"))
                    formattedvalue3=formattedvalue3.substring(1,formattedvalue3.length());
                if(formattedvalue4.startsWith("-"))
                    formattedvalue4=formattedvalue4.substring(1,formattedvalue4.length());
                if(formattedvalue5.startsWith("-"))
                    formattedvalue5=formattedvalue5.substring(1,formattedvalue5.length());


                tempString = mTextView.getText().toString();
                firstTemp = (Integer.toString(1) + ". " + formattedKey1 + " " + formattedvalue1 + "% $"+coin1+'\n');
                secondTemp = Integer.toString(2) + ". " + formattedKey2 + " " + formattedvalue2 + "% $"+coin2+'\n';
                thirdTemp = Integer.toString(3) + ". " + formattedKey3 + " " + formattedvalue3 + "% $"+coin3+'\n';
                fourthTemp = Integer.toString(4) + ". " + formattedKey4 + " " + formattedvalue4 + "% $"+coin4+'\n';
                fifthTemp = Integer.toString(5) + ". " + formattedKey5 + " " + formattedvalue5 + "% $"+coin5+'\n';
                total=tempString+firstTemp+secondTemp+thirdTemp+fourthTemp+fifthTemp;

                spannable = new SpannableString(total);
                Log.d("incoldtest",firstTemp);
                Log.d("incoldtest",secondTemp);
                Log.d("incoldtest",thirdTemp);
                Log.d("incoldtest",fourthTemp);
                Log.d("incoldtest",fifthTemp);


                value11.setTextColor(Color.GREEN);
                value11.setText(firstTemp);
                if(Float.parseFloat(value1.substring(0,value1.length()-1))>=0) {
                    val1=true;
                    value11.setTextColor(Color.GREEN);
                    value11.setText(firstTemp);
                }
                else{

                    value11.setTextColor(Color.RED);
                    value11.setText(firstTemp);
                }

                if(Float.parseFloat(value2.substring(0,value2.length()-1))>=0){
                    value22.setTextColor(Color.GREEN);
                    value22.setText(secondTemp);
                }
                else{
                    value22.setTextColor(Color.RED);
                    value22.setText(secondTemp);
                }
                if(Float.parseFloat(value3.substring(0,value3.length()-1))>=0){
                    value33.setTextColor(Color.GREEN);
                    value33.setText(thirdTemp);
                }
                else{
                    value33.setTextColor(Color.RED);
                    value33.setText(thirdTemp);
                }
                if(Float.parseFloat(value4.substring(0,value4.length()-1))>=0){
                    value44.setTextColor(Color.GREEN);
                    value44.setText(fourthTemp);
                }
                else{
                    value44.setTextColor(Color.RED);
                    value44.setText(fourthTemp);
                }
                if(Float.parseFloat(value5.substring(0,value5.length()-1))>=0){
                    value55.setTextColor(Color.GREEN);
                    value55.setText(fifthTemp);
                }
                else{
                    value55.setTextColor(Color.RED);
                    value55.setText(fifthTemp);
                }
            } catch (Exception e) {
                Log.d("mynewtestparse",e.toString());
            }

            // mTextView.setText(spannable,TextView.BufferType.SPANNABLE);
        }
    }

    public class FetchDataHot extends AsyncTask<String, Void, String> {


        @Override
        protected String doInBackground(String... params) {

            try {
                StringBuilder result = new StringBuilder();
                URL url = new URL("http://student04.cse.nd.edu:52109/crypto/hot");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String line;
                while ((line = rd.readLine()) != null) {
                    result.append(line);
                }
                rd.close();
                return result.toString();


            } catch (Exception e) {

            }
            return "hello";
        }

        protected void onPostExecute(String responseData) {
            Log.d("onpost", "RESPONSE DATA: " + responseData);
            JSONObject jsonO = null;
            try {
                jsonO = new JSONObject(responseData);
            } catch (Exception e) {

            }
            boolean val1;
            boolean val2;
            boolean val3;
            boolean val4;
            boolean val5;


            String key1;
            String value1;
            String key2;
            String value2;
            String key3;
            String value3;
            String key4;
            String value4;
            String key5;
            String value5;
            String tempString;
            String firstTemp;
            String secondTemp;
            String thirdTemp;
            String fourthTemp;
            String fifthTemp;
            String total;
            String price1;
            String price2;
            String price3;
            String price4;
            String price5;
            String coin1;
            String coin2;
            String coin3;
            String coin4;
            String coin5;

            Spannable spannable=null;
            Log.d("onpost", jsonO.toString());
            //for (int i = 0; i < jsonO.names().length()-1; i++) {
            try {
                Log.d("mytestparse",jsonO.getString("data"));
                String[] mykeys = jsonO.getString("data").split("\"");
                for(String key: mykeys)
                {
                    Log.d("mytestparse",key);

                }
                DecimalFormat df = new DecimalFormat("#0.00");
                Log.d("mynewparse",mykeys[1]);
                Log.d("mynewparse",mykeys[3]);
                Log.d("mynewparse",mykeys[5]);
                Log.d("mynewparse",mykeys[7]);
                Log.d("mynewparse",mykeys[9]);
                Log.d("mynewparse",mykeys[11]);
                Log.d("mynewparse",mykeys[13]);
                Log.d("mynewparse",mykeys[15]);
                Log.d("mynewparse",mykeys[17]);
                Log.d("mynewparse",mykeys[19]);
                Log.d("mynewparse",mykeys[4].substring(1,mykeys[4].length()-3));
                Log.d("mynewparse",mykeys[8].substring(1,mykeys[8].length()-3));
                Log.d("mynewparse",mykeys[12].substring(1,mykeys[12].length()-3));
                Log.d("mynewparse",mykeys[16].substring(1,mykeys[16].length()-3));
                Log.d("mynewparse",mykeys[20].substring(1,mykeys[20].length()-3));
                coin1= df.format(Float.parseFloat(mykeys[4].substring(1,mykeys[4].length()-3)));
                coin2= df.format(Float.parseFloat(mykeys[8].substring(1,mykeys[8].length()-3)));
                coin3= df.format(Float.parseFloat(mykeys[12].substring(1,mykeys[12].length()-3)));
                coin4= df.format(Float.parseFloat(mykeys[16].substring(1,mykeys[16].length()-3)));
                coin5= df.format(Float.parseFloat(mykeys[20].substring(1,mykeys[20].length()-3)));
                key1 = mykeys[1];
                value1 =mykeys[3];
                key2 = mykeys[5];
                value2 = mykeys[7];
                key3 = mykeys[9];
                value3 = mykeys[11];
                key4 = mykeys[13];
                value4 = mykeys[15];
                key5 = mykeys[17];
                value5 = mykeys[19];
                String formattedKey1 = String.format("%-5s",key1+":");
                String formattedKey2 = String.format("%-5s",key2+":");
                String formattedKey3 = String.format("%-5s",key3+":");
                String formattedKey4 = String.format("%-5s",key4+":");
                String formattedKey5 = String.format("%-5s",key5+":");

                DecimalFormat df2= new DecimalFormat("#00.00");
                String formattedvalue1 = df2.format(Float.parseFloat(value1.substring(0,value1.length()-1)));
                Log.d("mynewtestparse",formattedvalue1);
                String formattedvalue2 = df2.format(Float.parseFloat(value2.substring(0,value2.length()-1)));
                String formattedvalue3 = df2.format(Float.parseFloat(value3.substring(0,value3.length()-1)));
                String formattedvalue4 = df2.format(Float.parseFloat(value4.substring(0,value4.length()-1)));
                String formattedvalue5 = df2.format(Float.parseFloat(value5.substring(0,value5.length()-1)));
                if(formattedvalue1.startsWith("-"))
                    formattedvalue1=formattedvalue1.substring(1,formattedvalue1.length());
                if(formattedvalue2.startsWith("-"))
                    formattedvalue2=formattedvalue2.substring(1,formattedvalue2.length());
                if(formattedvalue3.startsWith("-"))
                    formattedvalue3=formattedvalue3.substring(1,formattedvalue3.length());
                if(formattedvalue4.startsWith("-"))
                    formattedvalue4=formattedvalue4.substring(1,formattedvalue4.length());
                if(formattedvalue5.startsWith("-"))
                    formattedvalue5=formattedvalue5.substring(1,formattedvalue5.length());


                tempString = mTextView.getText().toString();
                firstTemp = (Integer.toString(1) + ". " + formattedKey1 + " " + formattedvalue1 + "% $"+coin1+'\n');
                secondTemp = Integer.toString(2) + ". " + formattedKey2 + " " + formattedvalue2 + "% $"+coin2+'\n';
                thirdTemp = Integer.toString(3) + ". " + formattedKey3 + " " + formattedvalue3 + "% $"+coin3+'\n';
                fourthTemp = Integer.toString(4) + ". " + formattedKey4 + " " + formattedvalue4 + "% $"+coin4+'\n';
                fifthTemp = Integer.toString(5) + ". " + formattedKey5 + " " + formattedvalue5 + "% $"+coin5+'\n';
                total=tempString+firstTemp+secondTemp+thirdTemp+fourthTemp+fifthTemp;

                spannable = new SpannableString(total);
                Log.d("incoldtest",firstTemp);
                Log.d("incoldtest",secondTemp);
                Log.d("incoldtest",thirdTemp);
                Log.d("incoldtest",fourthTemp);
                Log.d("incoldtest",fifthTemp);


                value11.setTextColor(Color.GREEN);
                value11.setText(firstTemp);
                if(Float.parseFloat(value1.substring(0,value1.length()-1))>=0) {
                    val1=true;
                    value11.setTextColor(Color.GREEN);
                    value11.setText(firstTemp);
                }
                else{

                    value11.setTextColor(Color.RED);
                    value11.setText(firstTemp);
                }

                if(Float.parseFloat(value2.substring(0,value2.length()-1))>=0){
                    value22.setTextColor(Color.GREEN);
                    value22.setText(secondTemp);
                }
                else{
                    value22.setTextColor(Color.RED);
                    value22.setText(secondTemp);
                }
                if(Float.parseFloat(value3.substring(0,value3.length()-1))>=0){
                    value33.setTextColor(Color.GREEN);
                    value33.setText(thirdTemp);
                }
                else{
                    value33.setTextColor(Color.RED);
                    value33.setText(thirdTemp);
                }
                if(Float.parseFloat(value4.substring(0,value4.length()-1))>=0){
                    value44.setTextColor(Color.GREEN);
                    value44.setText(fourthTemp);
                }
                else{
                    value44.setTextColor(Color.RED);
                    value44.setText(fourthTemp);
                }
                if(Float.parseFloat(value5.substring(0,value5.length()-1))>=0){
                    value55.setTextColor(Color.GREEN);
                    value55.setText(fifthTemp);
                }
                else{
                    value55.setTextColor(Color.RED);
                    value55.setText(fifthTemp);
                }
            } catch (Exception e) {
                Log.d("mynewtestparse",e.toString());
            }

            // mTextView.setText(spannable,TextView.BufferType.SPANNABLE);
        }
    }

}
