
import os
import shutil

from BrisBot2 import Manager, AdminStats


def main(sqlite_filepath: str):
    db_manager = Manager(sqlite_filepath)

    db_manager.update_players(['user1', 'user2'], win=True, punteggio=78, minutes=12, seconds=6)
    db_manager.update_players(['user3'], win=False, punteggio=3, minutes=12, seconds=6)
    db_manager.update_players(['user4'], win=False, punteggio=39, minutes=12, seconds=6)

    db_manager.update_players(['user1'], win=False, punteggio=12, minutes=25, seconds=6)
    db_manager.update_players(['user2'], win=True, punteggio=108, minutes=25, seconds=6)

    print(db_manager.show_stats(username='user1'))
    print(db_manager.show_stats_admin(stat=AdminStats.PLAYER, username='user2'))
    print(db_manager.show_stats_admin(stat=AdminStats.TIME))
    print(db_manager.show_stats_admin(stat=AdminStats.WIN))
    print(db_manager.show_stats_admin(stat=AdminStats.TOT))
    print(db_manager.show_stats_admin(stat=AdminStats.SCORE))
    try:
        risultato = db_manager.show_stats_admin(stat=AdminStats.PLAYER)
        print(f"Se stampa questo, qualcosa non ha funzionato")
        print(risultato)
    except ValueError:
        print("Ok, c'è stato un errore nella statistica, proprio come atteso")
    print(db_manager.delete_player('user4'))
    try:
        print(db_manager.delete_player('user4'))
        print(f"Se stampa questo, qualcosa non ha funzionato")
    except Exception:
        print("Ok, c'è stato un errore nella cancellazione, proprio come atteso")


if __name__ == "__main__":
    db_path = "data/scores.db" # solo per resettare il test ad ogni riavvio
    db_base_path = os.path.dirname(db_path) # solo per resettare il test ad ogni riavvio
    if os.path.exists(db_base_path):
        shutil.rmtree(db_base_path) # solo per resettare il test ad ogni riavvio
    main(db_path)
