# git
  * Account bei https://github.com/ anlegen. 
  
  &lt;satire>_GitHub gehört Microsoft, sollte darum im Kanton St. Gallen datenschutzrechtlich unbedenklich sein, im Gegensatz zum Anzeigen des eigenen Dateinamens auf den Schuldruckern_&lt;/satire>.

  * ssh-Key generieren und auf git deponieren. Siehe https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
  * evtl 2FA aktivieren (der Microsoft Authenticator kann dafür verwendet werden).
  * Ihren Usernamen Herrn Blöchliger mitteilen, damit er Ihnen Zugriff auf dieses Repo geben kann.
  * `git-bash` starten und mit `cd` in ein geeignets Verzeichnis navigieren, dann auschecken:
  ```
git clone git@github.com:techlabksbg/xmaslights.git
cd xmaslights
code .
  ```
  * Nötige Konfiguration von `git`:
    * TODO
  * Änderungen vornehmen, dann in der `git-bash`
    * `git add `_datei_
    * `git commit -m '`_Kurzbeschreibung der Änderung_`'`
    * `git push`

