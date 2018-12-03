package com.example.aquariumapp.UI;

import android.util.Log;

import com.example.aquariumapp.Model.Aquarium;
import com.example.aquariumapp.Network.NetworkManager;

import java.util.List;

import io.reactivex.SingleObserver;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;

//presenter similar to controller. MVP MODEL VIEW PRESENTER.
public class AquariumPresenterImpl implements AquariumContract.Presenter {

    private AquariumContract.View view;
    private NetworkManager networkManager;

    public AquariumPresenterImpl(AquariumContract.View view, NetworkManager networkManager) {
        this.view = view;
        this.networkManager = networkManager;
    }

    @Override
    public void getData() {


       networkManager.getAquariumData()
               .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(new SingleObserver<List<Aquarium>>() {
        @Override
        public void onSubscribe(Disposable d) {

        }

        @Override
        public void onSuccess(List<Aquarium> aquarium) {

            view.update(aquarium.get(0));
        }

        @Override
        public void onError(Throwable e) {
            Log.d("", "onError: An error occured when connecting to host webpage");
            Log.e("ERR: ", e.getMessage());
        }
    });
//}
    }
}