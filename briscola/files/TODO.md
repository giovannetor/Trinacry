# Schema del Database:
## Tabella scores
- [x] **username:** <ins>varchar</ins> *Nome utente del giocatore*
- [x] **score:** <ins>int</ins> *Punteggio del giocatore*
- [x] **win:** <ins>int</ins> *Contatore delle partite vinte dal giocatore*
- [x] **tot:** <ins>int</ins> *Contatore delle partite giocate*
- [x] **time:** <ins>long</ins> *Tempo di gioco in millisecondi*

# Funzioni necessarie:
- [x] **cont_scores:** questa funzione deve prendere i valori delle carte conquistate dai giocatori (vincitori e vinti), e aggiungerli al contatore totale nel database (in caso di team formati da 2 persone, i punti vanno sommati a entrambi). 
  - INPUT: team_members, punteggio
  - Se uno username non è presente nel database lo crea e inizializza tutti i valori a zero e poi aggiorna
- [x] **cont_win:** aggiunge +1 al contatore delle partite VINTE nel db ai giocatori membri del team vincente. 
  - INPUT: lista di usernames
  - Se uno username non è presente nel database lo crea e inizializza tutti i valori a zero e poi aggiorna
- [x] **cont_tot:** aggiunge +1 al contatore delle partite TOT nel db a tutti i giocatori nella partita. 
  - INPUT: lista di usernames
  - Se uno username non è presente nel database lo crea e inizializza tutti i valori a zero e poi aggiorna
- [x] **cont_time:** aggiunge il tempo della durata della partita al contatore totale di ogni giocatore nella partita. 
  - INPUT: integers in formato hh:mm:ss
  - Se uno username non è presente nel database lo crea e inizializza tutti i valori a zero e poi aggiorna
- [x] **show_stats:** permette a un utente di richiamare tutte le sue statistiche.
- [x] **show_stats_admin:** permette a un admin di richiamare tutte le statistiche di tutti i giocatori, ordinate in base al parametro passato come argomento. (es. .ssa giovannetor ritornerebbe le mie statistiche. .ssa win ritornerebbe la classifica di giocatori con più vittorie.)

# Informazioni necessarie:
- **cont_scores:**
  - team_members (un array con tutti i membri del team)  <-- Ogni array sarà una lista formato "[nick1 , (nick2)]" . Il nick2 non sarà sempre presente.
  - Punteggio da sommare (Il punteggio va come secondo parametro della funzione)
- **show_stats_admin:** Specificare i parametri secondo cui ordinare i risultati
  - win
  - player
  - time
  - score
  - max_results = 10
