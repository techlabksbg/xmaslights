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
    * Usernamen setzen (öffentlich sichtbar in den commits):
```
git config --global user.name "Mona Lisa"
```
  * Änderungen vornehmen, dann in der `git-bash`
    * `git add `_datei_
    * `git commit -m '`_Kurzbeschreibung der Änderung_`'`
    * `git push`

## Branches
Neuen branch anlegen
```
git checkout -b neuer_branch
```
Änderungen vornehmen, committen, push
```
git push --set-upstream origin neuer_branch
```

### Merge oder rebase?
Siehe auch https://blog.git-init.com/differences-between-git-merge-and-rebase-and-why-you-should-care/

Vor dem mergen (oder rebase) dafür sorgen,
dass der aktuelle Branch sauber ist:
```
git status
```

Sonst Änderungen noch adden, committen oder verwerfen mit:
```
git checkout eineDatei
```
oder Dateien "stashen" oder etwas rabiater 
im Wurzelverzeichnis des Repos alle Änderungen
verwerfen:
```
git restore .
```

Änderung von einem anderen Branch importiern.
```
git checkout mein_branch
git merge anderer_branch
```

Einzelne Datei in den main-branch importieren. Dazu erst im eigenen Branch
(hier meinBranch genannt) alles sauber machen (commiten oder Änderungen
verwerfen). Dann
```bash
git checkout main
git pull
git checkout meinBranch meineDatei.py
git add meineDatei.py
git commit -m 'super duper Animation'
git push
```


