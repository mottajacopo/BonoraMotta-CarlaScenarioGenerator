# MottaBonora-CarlaScenarioGenerator


**Links:**  
	Carla github                    https://github.com/carla-simulator/carla  
	Carla 0.9.11                    https://github.com/carla-simulator/carla/releases/tag/0.9.11  
	Carca documentation             https://carla.readthedocs.io/en/latest/  
	Scenario Runner github          https://github.com/carla-simulator/scenario_runner  
	Scenario Runner 0.9.11 		https://github.com/carla-simulator/scenario_runner/releases/tag/v0.9.11  
	Scenario Runner documentation   https://carla-scenariorunner.readthedocs.io/en/latest/  
	Pyoscx github                   https://github.com/pyoscx/pyoscx  
	ScenarioGeneration              https://github.com/pyoscx/scenariogeneration

# Carla

**Installazione :**  
- scaricare e estrarre CARLA_0.9.11.zip 
- scaricare AdditionalMaps_0.9.11.zip e estrarre nella cartella di Carla
- editare variabili di sistema:
       aggiungere una variabile chiamata PYTHONPATH con i seguenti percorsi in base
       alla disposizione delle proprie cartelle e alla versione di carla che si vuole utilizzare:
       
     ![PYTHONPATH](https://github.com/mottajacopo/MottaBonora-CarlaScenarioGenerator/blob/main/images/pythonpath.png)
     
Nota:  
Modificare il path della variabile di ambiente in base alla coppia (carla + scenario runner) di versioni che si vuole usare.   
Occorre che la versione di carla in uso sia nella cartella C:\Carla0.9.11 .  
Di conseguenza occorre anche modificare il nome del file .EGG nella variabile di ambiente PYTHONPATH con il numero di versione corretto.  
     
 # Carla usage

**1-** Aprire il cmd nella cartella di Carla (sul desktop)
	Lanciare il server con il seguente comando:
	
	CarlaUE4.exe -quality-level=High

**2-** Aprire il cmd nella cartella PythonAPI/util
	Lanciare il seguente comando per scegliere la mappa (la milgiore è town05):
	
	python config.py --map Town05

**3-** Aprire il cmd nella cartella PythonAPI/examples
	Lanciare il seguente comando per polopare la mappa:
	
	python spawn_npc.py -n 50 -w 15    #spawna 50 vehicles and 15 pedestrians

**4-** Aprire il cmd nella cartella PythonAPI/examples
	Lanciare il seguente comando per abilitare il meteo e l'ora del giorno dinamica:
	
	python dynamic_weather.py

**5-** Aprire il cmd nella cartella PythonAPI/examples
	Lanciare il seguente comando per avviare il client in guida manuale
	
	python manual_control.py 

**6-** Una volta nel client:

	 P            : toggle autopilot
 	 TAB          : change sensor position (mettere camera frontale)
     C            : change weather (funziona se dynamic weather è disabilitato)
     F1           : toggle HUD
     R            : toggle recording (frame as jpg)


# Scenario Generation
