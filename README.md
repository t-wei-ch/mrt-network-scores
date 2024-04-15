# A Tool for Computing Distance to Target Stations in the Singapore MRT Network

## About

This is a tool that uses [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) to find the shortest path from any MRT station to a given subset of MRT stations, termed here the `target_stations`. The implementation is credited to Eryk Kopczyński, code referenced from [here](https://www.python.org/doc/essays/graphs/).

For the purposes of modelling the inconvenience of transiting and/or train waiting times, transits between different lines at the same stations count as an additional station for the purposes of computing the score.

The score of a `station` is defined to be the minimal number of stations (including transits) from `station` to any station in `target_stations`, and the MRT network being used is up-to-date as of 16 April 2024.

## Structure

This repository consists of two folders: 
1. `code`, containing the `mrt_tools.py` script and the `mrt_scores.ipynb` notebook;
2. `scores`, containing the `mrt_scores` csv file.

## How to use

Firstly, clone this repository to your desired location.

By default, `mrt_scores.csv` in the `scores` folder contains the scores for the following stations: 

|Line|Station(s)|
|---|---|
|NSL|Raffles Place, City Hall, Marina Bay|
|EWL|Outram Park, Tanjong Pagar, Raffles Place, City Hall|
|CCL|Telok Blangah, Harbourfront, Bayfront, Promenade, Esplanade, Marina Bay|
|DTL|Telok Ayer, Downtown, Bayfront, Promenade|
|TEL|Maxwell, Shenton Way, Marina Bay|

As a user of this tool, only the notebook `mrt_scores.ipynb` would be used for running the script to generate the table of scores. Simply updating the `target_stations` variable in the notebook with your desired list of target stations to compute the distance to, and then hitting "Run All" would update the scores accordingly in `mrt_scores.csv`.
