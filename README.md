# 📹 Guardian-Garden 🏡

Benvenuto in Guardian-Garden! Questa applicazione è progettata per aiutarti a individuare potenziali individui sospetti all'interno delle tue aree residenziali private.

Per una visione più dettagliata, consulta la presentazione inclusa nel repository con il nome "Guardian-Garden Presentation.pdf".

## Prerequisiti
- Sistema operativo: Windows
- Dispositivo video funzionante

## Installazione
Per iniziare, clona il repository sul tuo sistema locale con il seguente comando:

```bash
git clone https://github.com/ItsAtlant/Guardian-Garden.git
```

Successivamente, scarica i requisiti necessari elencati nel file requirements.txt.

## Configurazione
Apri il file config.json e inserisci le tue credenziali (email e password). Regola i parametri di sensibilità per personalizzare il rilevamento di individui sospetti:

- `sensibilità_faccia_sconosciuta`: Imposta questo valore per regolare il timer quando c'è uno sconosciuto nel giardino con faccia identificabile.
- `sensibilità_senza_faccia`: Imposta questo valore per regolare il timer quando c'è uno sconosciuto mascherato.

Assicurati di inserire le foto della cerchia autorizzata nella cartella "foto" per evitare che individui autorizzati vengano identificati erroneamente come estranei.

## Utilizzo
Esegui il programma con il comando:

```bash
python main.py
```

Durante l'esecuzione del programma:
- Premi 'f' per attivare o disattivare il riconoscimento facciale.
- Premi 'q' per interrompere il programma.

## Segnalazione di Problemi
Se incontri problemi o hai suggerimenti, apri una nuova issue nel repository su GitHub: [Guardian-Garden Issues](https://github.com/ItsAtlant/Guardian-Garden/issues).

Grazie per aver scelto Guardian-Garden! 🌳👀
