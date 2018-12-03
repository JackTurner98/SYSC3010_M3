package com.example.aquariumapp.UI;

import com.example.aquariumapp.Model.Aquarium;

//interface between view and controller class
public interface AquariumContract {
    // interface and presenter can only use these local functions.
    // promotes low coupling
    interface View {
        void update(Aquarium aquarium);
    }

    interface Presenter {
        void getData();
    }
}
