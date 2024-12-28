import threading
import time
import os
from yt_dlp import YoutubeDL
from datetime import datetime
import random

class WorkerThread(threading.Thread):
    """Thread qui effectue une tâche et peut être arrêté proprement."""
    def __init__(self, stop_event, url, ydl_opts, url_list, filename, processed_filename):
        super().__init__()
        self.stop_event = stop_event
        self.url = url
        self.ydl = ydl_opts
        self.url_list = url_list
        self.filename = filename
        self.processed_filename = processed_filename

    def run(self) -> None:
        ydl = self.ydl
        retry_delay = random.randint(1, 5)
        url = self.url
        print("Le thread a démarré.")
        while not self.stop_event.is_set():  # Vérifie si un arrêt est demandé
            while True:
                print("Le thread est en cours d'exécution...")
                print("utilisation nouvelle url: ", url)
                start_time = time.time()
                try:
                    print(f"\n📥 Traitement de l'URL : {url}")
                    # Extraire les informations du post Reddit
                    info_dict = ydl.extract_info(url, download=False)
                    # Vérifier si le post contient des vidéos
                    if 'entries' in info_dict:
                        is_video_found = False
                        for entry in info_dict['entries']:
                            if entry.get('ext') == 'mp4' or entry.get('is_video', False):
                                print(f"✅ Vidéo trouvée, téléchargement en cours : {entry['url']}")
                                ydl.download([entry['url']])
                                is_video_found = True
                                break
                        if not is_video_found:
                            print(f"❌ Aucun contenu vidéo valide trouvé dans : {url}")
                    elif info_dict.get('ext') == 'mp4' or info_dict.get('is_video', False):
                        print(f"✅ Vidéo trouvée, téléchargement en cours : {url}")
                        ydl.download([url])
                    else:
                        print(f"❌ L'URL ne contient pas de vidéo valide : {url}")
                    break
                except Exception as e:
                    if "HTTP Error 429" in str(e):
                        print(f"❌ Erreur 429 pour {url}. Attente de {retry_delay} secondes avant de réessayer...")
                        time.sleep(retry_delay)
                    else:
                        print(f"❌ Erreur lors du traitement de {url} : {e}")
                        break
            self.stop_event.set()

            # Une fois le traitement terminé, ajouter l'URL au fichier "lien_traite.txt"
            with open(self.processed_filename, 'a') as f_processed:
                f_processed.write(url + "\n")

            # Une fois le traitement terminé, supprimer l'URL de la liste
            if url in self.url_list:
                self.url_list.remove(url)

            # Réécrire le fichier sans l'URL traitée
            with open(self.filename, 'w') as f:
                for u in self.url_list:
                    f.write(u + "\n")

        print("Le thread s'est arrêté proprement.")


def action(urls, ydl_opts, filename, processed_filename):
    salut = []
    index = 0
    total_urls = len(urls)
    with YoutubeDL(ydl_opts) as ydl:
        while index < total_urls:
            for _ in range(4):
                if index < total_urls:
                    url = urls[index]
                    # Création de l'événement d'arrêt
                    stop_event = threading.Event()
                    # Démarrage du thread
                    worker = WorkerThread(stop_event, url, ydl, urls, filename, processed_filename)
                    salut.append(worker)
                    worker.start()
                    index += 1
                    time.sleep(5)
        # Simulation du programme principal
        time.sleep(60)  # Attendre un peu pour les tests
        # Demander au thread de s'arrêter
        try:
            for worker in salut:
                print("Demande d'arrêt du thread.")
                worker.stop_event.set()
                print("Le thread a été arrêté.")
                worker.join()
        except:
            print("Demande d'arrêt du thread.")
            stop_event.set()
            # Attendre la fin du thread
            worker.join()
            print("Le thread a été arrêté.")

"""------------------------------------------------------------------------------------------"""
def download_reddit_videos(file_with_urls, output_folder, delay=5, retry_delay=60):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_folder, '%(title)s_' + current_time + '.%(ext)s'),  # Ajouter la date et l'heure
        'noplaylist': True,
        'ignore_errors': True,
        'verbose': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    with open(file_with_urls, 'r') as f:
        urls = f.read().splitlines()
    return urls, ydl_opts


# Chemin vers le fichier contenant les URLs
url_file = "urls.txt"
processed_file = "lien_traiter.txt"  # Fichier pour les URLs traitées
output_dir = "reddit_video"
os.makedirs(output_dir, exist_ok=True)
urls, ydl_opts = download_reddit_videos(url_file, output_dir, delay=3, retry_delay=6)
action(urls, ydl_opts, url_file, processed_file)
