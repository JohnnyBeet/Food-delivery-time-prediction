data{
    int N;                          // Number of samples
    vector[N] distance;             // Distances
    vector[N] meal_preparation_time; // Meal preparation times
    vector[N] delivery_times;       // Delivery times
    array[N] int traffic_level;           // Traffic levels
}

parameters{
    real distance_coeff;
    real mean;
    vector[4] traffic_level_coeff;
    real meal_prep_coeff;
    real<lower=0> sigma;
}

transformed parameters {
    vector[N] mu;
    for(i in 1:N){
        mu[i] = exp(distance_coeff * distance[i] + traffic_level_coeff[traffic_level[i]] + meal_prep_coeff * meal_preparation_time[i]+mean);
    }

}

model{
    mean ~ normal(3, 0.1);
    distance_coeff ~ normal(0,0.5);
    meal_prep_coeff ~ normal(0,0.5);
    sigma ~ exponential(0.5);
    delivery_times ~ inv_gamma(pow(mu, 2) / pow(sigma, 2) + 2, pow(mu,3) / pow(sigma, 2) + mu);
    traffic_level_coeff[1] ~ normal(0, 0.5);
    traffic_level_coeff[2] ~ normal(0, 0.5);
    traffic_level_coeff[3] ~ normal(0, 0.5);
    traffic_level_coeff[4] ~ normal(0, 0.5);
}

generated quantities {
    vector[N] delivery_time;
    vector[N] log_lik;
    for (i in 1:N){
        delivery_time[i] = inv_gamma_rng(pow(mu[i], 2) / pow(sigma, 2) + 2, pow(mu[i],3) / pow(sigma, 2) + mu[i]);
        log_lik[i] = inv_gamma_lpdf(delivery_times[i] | pow(mu[i], 2) / pow(sigma, 2) + 2, pow(mu[i],3) / pow(sigma, 2) + mu[i]);
    }
}