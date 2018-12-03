package com.example.aquariumapp.Network;

import com.example.aquariumapp.Model.Aquarium;

import java.util.List;

import io.reactivex.Single;
import retrofit2.http.GET;

public interface AquariumAPIService {
    //Retrieves what's on the /getData and return an object of type Aquarium or throw an error (due to Single)
    @GET("getData")
    Single<List<Aquarium>> getAquariumData();
}
