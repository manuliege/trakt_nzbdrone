trakt_nzbdrone
==============

script to send downloaded notifications to trakt for episodes downloaded by nzbdrone

First, you have to modify the .ini with your information (trakt login, ...).

You may then execute this script (python 2.7) :
it will take a moment for the first run if your history in nzbdrone is big (many imported episodes to notify).
If you already set those episodes or some of them as "downloaded" in trakt, this script won't change anything :
the only modifications made in trakt are for the downloaded episodes in nzbdrone not yet set so in trakt.

At the end of the execution, there's a pause of 5' and then the operation starts again,
but this time to send only the new notifications (new episodes imported in nzbdrone since the last run).

You stop the script at any time the usual way.

If you get an error about the db, please update your DLL sqlite in your python installation.
