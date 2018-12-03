package com.example.aquariumapp.Network;

import com.example.aquariumapp.Model.Aquarium;
import com.jakewharton.retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;

import java.util.List;

import io.reactivex.Single;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class NetworkManager {

    //Network Manager is dealing with setting up API service
    private AquariumAPIService service = new Retrofit.Builder()
            .baseUrl("https://immense-waters-37972.herokuapp.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
            .client(new OkHttpClient()) //http protocol stuff
            .build()
            .create(AquariumAPIService.class);

    //Gets Aquarium object or throws an error
    public Single<List<Aquarium>> getAquariumData () {
        return service.getAquariumData();
    }
}
