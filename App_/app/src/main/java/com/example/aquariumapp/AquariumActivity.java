package com.example.aquariumapp;

import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.example.aquariumapp.Model.Aquarium;
import com.example.aquariumapp.Network.NetworkManager;
import com.example.aquariumapp.UI.AquariumContract;
import com.example.aquariumapp.UI.AquariumPresenterImpl;

public class AquariumActivity extends AppCompatActivity implements AquariumContract.View {

    private AquariumContract.Presenter presenter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_aquarium);
        presenter = new AquariumPresenterImpl(this,new NetworkManager());
    }

    public void updateData(View view){
        presenter.getData();
    }

    @Override
    public void update(Aquarium aquarium) {
        TextView temperature = findViewById(R.id.temperatureText);
        TextView waterLevel = findViewById(R.id.waterLevelText);
        TextView overflowLevel = findViewById(R.id.overflowLevelText);

        //get notification textviews
        TextView errOverflow = findViewById(R.id.ovrflowerrText);
        TextView errWaterlvl = findViewById(R.id.waterlvlerrText);
        TextView errTemp = findViewById(R.id.temperrText);
        TextView allGood = findViewById(R.id.allGoodText);


        //clear color
        overflowLevel.setTextColor(Color.WHITE);
        waterLevel.setTextColor(Color.WHITE);
        temperature.setTextColor(Color.WHITE);

        //clear notifications
        errOverflow.setText("");
        errWaterlvl.setText("");
        errTemp.setText("");
        allGood.setText("");


        temperature.setText("Temperature: " + aquarium.getTemperature() + "°C");
        waterLevel.setText("Water Level: " + aquarium.getWaterLevel() + "cm");
        overflowLevel.setText("Overflow Level: " + aquarium.getOverflowLevel() + "cm");


        String ovrflowValue = aquarium.getOverflowLevel();
        double ovrflowresult = Double.parseDouble(ovrflowValue);
        if(ovrflowresult >= 2){
            overflowLevel.setTextColor(Color.RED);
            errOverflow.setText("- Check filter for blockage. Water prone to overflowing");
        }


        String waterlvlValue = aquarium.getWaterLevel();
        double waterlvlResult = Double.parseDouble(waterlvlValue);
        if(waterlvlResult <= 2){
            waterLevel.setTextColor(Color.RED);
            errWaterlvl.setText("- Water Level is dropping, please refill the aquarium soon");
        }

        String tempValue = aquarium.getTemperature();
        double tempResult = Double.parseDouble(tempValue);
        if(tempResult > 30 || tempResult < 20){
            temperature.setTextColor(Color.RED);
            errTemp.setText("- Optimal temperature is between 24 - 28 degrees celsius");
        }

        if(ovrflowresult < 2 && waterlvlResult > 2 && tempResult < 30 && tempResult > 20){
            allGood.setText("Your aquarium is healthy and well :) YOU ROCK!!");
        }
    }
}
