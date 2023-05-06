# SpotiFyre

*Team: Algorithmic Alliance*

Contributors | Github usernames  
--- | ---
Chinmay Agrawal | [ch1nmay7898](https://github.com/ch1nmay7898) 
Medha Rudra | [MedhaRudra](https://github.com/MedhaRudra), [medha-rudra](https://github.com/medha-rudra)
Mukund Kalantri | [mukundkalantri23](https://github.com/mukundkalantri23)
Tejas Kaushik | [tejas1812](https://github.com/tejas1812), [teka7939](https://github.com/teka7939)
Utsav Atul Gupta | [MrUtsavG](https://github.com/MrUtsavG)

Spotify Playlist creator for large groups.

Demo Video: [Link](https://cuboulder.zoom.us/rec/share/muq3Ob7HjhebfACosuPsMVUB0Vttgc8HMzUNgfpMOYXztzxcE2I65NdqvYnGgdhl.bDYrYYYP8uYbrt4L)

## Architecture Diagram

![Architecture Diagram](/images/Architecture_diagram.png)

## Rubric 

Rubric Name | Link 
--- | ---
Web application basic form, reporting | [React app js file](/web_ui_app/src/App.js)<br>
Data collection | [Spotify Listen history collection](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/spotify_login.py)<br> 
Data analyzer | [Listening history analysis and playlist creation](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/playlist.py)<br> 
Unit tests | [Unit tests for groups feature](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/tests/)<br> 
Data persistence | [Postgres Helm Chart](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/tree/main/infra/postgresql)<br>
Rest collaboration internal or API endpoint: | [Auth APIs](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/auth.py), [Group Managements APIS](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/main.py), [Playlist APIs](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/playlist.py), [Spotify APIS](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/spotify_login.py) <br>
Product environment:| https://web-ui-app-je6wfb672a-uc.a.run.app <br>
Integration tests | [DB integration tests](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/tests/test_db_integration.py) <br> 
Using mock objects or any test doubles | [Main unit test](/services/login_backend/tests/test_main.py)<br>
Acceptance tests | [Acceptance test](/services/login_backend/tests/test_acceptance.py)<br>
Event collaboration messaging | [Publisher](/services/login_backend/playlist.py), [Subscriber](/services/playlist/subscriber.py)

### Continuous integration (Using jenkins)

![Jenkins integration pipeline](/images/ci_1.png)

### Continuous delivery (Using [Google Cloud Build](https://console.cloud.google.com/cloud-build/builds;region=global?query=trigger_id%3D%22f7e1a49c-6542-42d5-b278-32be4a149b07%22&authuser=5&project=fse-new))

![](/images/cd_1.png)

### Production monitoring and instrumenting

![](/images/monitoring_1.png)

![](/images/monitoring_2.png)

