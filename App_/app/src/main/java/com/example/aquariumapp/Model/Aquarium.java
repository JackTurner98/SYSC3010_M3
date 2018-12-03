package com.example.aquariumapp.Model;

public class Aquarium {
    private String Temperature;
    private String waterLevel;
    private String overflowLevel;


    public Aquarium(String temperature, String waterLevel, String overflowLevel) {
        this.Temperature = temperature;
        this.waterLevel = waterLevel;
        this.overflowLevel = overflowLevel;
    }

    public String getTemperature() {
        return Temperature;
    }

    public void setTemperature(String temperature) {
        this.Temperature = temperature;
    }

    public String getWaterLevel() {
        return waterLevel;
    }

    public void setWaterLevel(String waterLevel) {
        this.waterLevel = waterLevel;
    }

    public String getOverflowLevel() { return overflowLevel; }

    public void setOverflowLevel(String overflowLevel) { this.overflowLevel = overflowLevel; }
}
