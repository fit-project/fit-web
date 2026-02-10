# Perché **sslkey.log** non deve far parte dell’acquisizione forense  
_Esempio concreto e motivazione tecnico‑giuridica_

---

## Punto di partenza

Questa nota nasce dalla domanda:

> **“Perché non ho inserito `sslkey.log` nell’acquisizione forense?”**

La risposta non è teorica, ma **pratica, concreta e difendibile in aula di tribunale**.

Di seguito viene illustrato uno **scenario reale**, che mostra chiaramente perché  
`sslkey.log` è diverso da `acquisition.log` e perché **inserirlo crea un problema che oggi non esiste**.

---

## Scenario reale

Stai effettuando un’acquisizione forense di una pagina web HTTPS  
(ad esempio un’area riservata di un servizio online).

Nella tua acquisizione alleghi i seguenti file:

- `acquisition_page.wacz`
- `acquisition_video.mp4`
- `acquisition.pcap`
- `headers.txt`
- `server.cer`
- `sslkey.log`

Tutti i file sono:
- presenti nella directory di acquisizione  
- hashati  
- formalmente “congelati”  

---

## Arriva la controparte (avvocato / perito)

### Prima domanda (semplice, devastante)

> **“Conferma che grazie al file `sslkey.log` è possibile decifrare integralmente il traffico HTTPS contenuto nel PCAP?”**

Risposta tecnica corretta: **sì**.

Non è possibile rispondere diversamente.

---

### Seconda domanda (qui nasce il problema)

> **“Conferma che nel traffico HTTPS decifrabile potrebbero essere presenti dati personali, cookie di sessione, token di autenticazione o altri contenuti non esplicitamente indicati come oggetto dell’acquisizione?”**

Risposta tecnica corretta: **sì**.

Anche in questo caso, non è possibile rispondere “no”.

---

### Terza domanda (il colpo finale)

> **“Per quale motivo tali dati, pur essendo tecnicamente accessibili grazie ai file da voi prodotti, non sono stati dichiarati come oggetto dell’acquisizione forense?”**

⚠️ **Qui nasce una difficoltà reale**.

Perché:
- hai fornito **i mezzi tecnici** per accedervi  
- ma **non li hai qualificati**  
- e **non ne hai delimitato il perimetro**  

Questo apre un problema serio sul piano giuridico e probatorio.

---

## Confronto diretto con `acquisition.log`

### Domanda analoga

> **“Grazie al file `acquisition.log` è possibile accedere a ulteriori dati rispetto a quelli dichiarati?”**

Risposta:

> **“No. Il file descrive esclusivamente le operazioni del sistema.”**

Fine della questione.  
Nessun ampliamento, nessun rischio.

---

## Il punto chiave (concreto)

`sslkey.log` **non è pericoloso perché esiste**.  
È pericoloso perché **consente di fare qualcosa in più**.

In ambito forense questo si definisce:

> **Ampliamento implicito del perimetro probatorio**

Ed è **esattamente ciò che va sempre evitato**.

---

## Analogia ultra concreta

Immagina di:

- depositare **una registrazione telefonica**
- e, insieme, consegnare **le credenziali dell’account cloud** da cui è possibile scaricare *tutte* le chiamate

Tu dichiari:

> “Io ho acquisito solo questa chiamata.”

La controparte risponde:

> “Sì, ma ci ha fornito le chiavi per ottenerne molte altre.”

È **la stessa identica situazione**.

---

## In poche parole sslkey.log non è stato inserito perché

> **Un file che abilita l’accesso a dati non esplicitamente acquisiti non deve far parte dell’acquisizione forense.**

### Applicazione concreta

- `sslkey.log`
  - abilita decifrazione  
  - abilita accesso  
  - abilita ampliamento  

- `acquisition.log`
  - non abilita nulla  
  - descrive soltanto  

---

## Conclusione netta

- Inserire `sslkey.log` **espone a rischi**
- Non inserirlo **non indebolisce la prova**
- Inserirlo **Obbliga a giustificare dati che oggi non esistono**
- La controparte **Potrebbe usare questo punto a suo favore**

Questo è il punto esatto in cui si passa da:
> *tool tecnico che funziona*

a:

> **strumento forense maturo**

---
