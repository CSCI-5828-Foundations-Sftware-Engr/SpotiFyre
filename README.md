# SpotiFyre
Spotify Playlist creator for large groups

## Architecture Diagram
![Architecture Diagram](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/Architecture_diagram.png?raw=true)

## Rubric 

Rubric Name | Link 
--- | ---
Web application basic form, reporting | <br>
Data collection | [Spotify Listen history collection](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/spotify_login.py)<br> 
Data analyzer | [Listening history analysis and playlist creation](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/playlist.py)<br> 
Unit tests | [Unit tests for groups feature](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/tests/test_main.py)<br> 
Data persistence | [Postgres Helm Chart] (https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/tree/main/infra/postgresql)<br>
Rest collaboration internal or API endpoint: | [Auth APIs](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/auth.py), [Group Managements APIS](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/main.py), [Playlist APIs](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/playlist.py), [Spotify APIS](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/spotify_login.py) <br>
Product environment:| https://web-ui-app-je6wfb672a-uc.a.run.app <br>
Integration tests | [DB integration tests](https://github.com/CSCI-5828-Foundations-Sftware-Engr/SpotiFyre/blob/main/services/login_backend/tests/test_db_integration.py) <br> 
Using mock objects or any test doubles | <br>
Continuous integration | <br>
Production monitoring | <br>
instrumenting | <br>
![](/monitoring_1.png)
![](/monitoring_2.png)
Acceptance tests | <br>
Event collaboration messaging | <br>
Continuous delivery |<br>
