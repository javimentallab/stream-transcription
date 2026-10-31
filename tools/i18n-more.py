# Translations beyond English and Spanish, read by tools/i18n-messages.py.
# One "key|text" per line; {0}, {1}… are placeholders and must match the English text.
# Model names, "WhisperLive", "Hugging Face", "VRAM", "int8", "faster-whisper", ".srt" stay as they are.

LANGS = {}

LANGS['pt_BR'] = """
extName|Stream Transcription
extDescription|Legendas ao vivo para qualquer aba, transcritas e traduzidas pelo seu próprio servidor Whisper.
start|Ativar legendas
stop|Desativar legendas
status_idle|Pronto
status_connecting|Conectando…
status_loading|Carregando o modelo…
status_listening|Ouvindo…
status_live|Ao vivo
status_stalled|Áudio parado
status_error|Erro
status_noresponse|Sem resposta
model|Modelo
model_server_default|O do servidor
model_default_tag|{0} · padrão
manage_models|Gerenciar modelos
spoken_lang|Idioma do áudio
auto_detect|Automático
detected|Detectado: {0}
subs_lang|Legendas em
original_lang|Sem tradução
lines|Linhas
text_size|Tamanho do texto
save_srt|Salvar as legendas (.srt) ao parar
advanced|Avançado
use_vad|Pular silêncios (detecção de voz)
settings|Configurações
first_load_hint|Na primeira vez, um modelo pode levar até um minuto para carregar.
options_locked|Desative as legendas para mudar estas opções.
server_setup_title|Conecte seu servidor
server_setup_hint|O Stream Transcription precisa de um servidor WhisperLive rodando no seu computador ou na sua rede.
server_address|Endereço do servidor
server_placeholder|ex.: localhost:9090 ou 192.168.1.10:9090
connect|Conectar
server_ok_models|Conectado · {0} modelos
server_ok_one_model|Conectado · 1 modelo
server_plain|Conectado · WhisperLive padrão (sem gerenciamento de modelos)
server_checking|Verificando…
server_unreachable|Não foi possível conectar ao servidor. Ele está ligado? Verifique o endereço e o firewall.
server_timeout|O servidor não respondeu a tempo.
server_bad_url|Esse endereço não é válido.
server_change|Alterar
server_help|Como monto um servidor?
server_help_1|Você precisa de um servidor WhisperLive (livre e gratuito) rodando em um computador, de preferência com placa de vídeo NVIDIA. Modelos pequenos também funcionam só com o processador.
server_help_2|Depois digite aqui o endereço dele: o IP do computador e a porta, ex.: 192.168.1.10:9090. Se estiver neste mesmo computador, localhost:9090.
server_help_3|Para baixar e gerenciar modelos por esta página, adicione ao servidor o complemento do Stream Transcription.
server_help_guide|Guia passo a passo
error_capture|Esta aba não pode ser capturada (páginas do navegador, lojas de extensões e PDFs não são permitidos).
error_no_media|Não há vídeo nem áudio nesta página.
error_server_full|O servidor está ocupado. Espera estimada: {0} min.
error_disconnected|O servidor fechou a conexão.
error_model_load|⚠ Não há memória de vídeo (VRAM) suficiente no servidor para este modelo. Escolha um modelo menor ou ative “Economizar memória (int8)” em Avançado.
warn_no_response|⚠ As legendas pararam de chegar, embora haja som. Provavelmente o modelo não cabe na memória de vídeo (VRAM) do servidor: escolha um modelo menor ou ative “Economizar memória (int8)” em Avançado.
warn_slow_load|⚠ O modelo está demorando demais para carregar. Pode não caber na memória de vídeo (VRAM) do servidor: escolha um modelo menor ou ative “Economizar memória (int8)” em Avançado.
error_reload|Recarregue a página (F5) e comece de novo.
error_no_server|Primeiro configure o servidor.
settings_title|Stream Transcription · Configurações
section_server|Servidor
section_models|Modelos
section_subtitles|Legendas
section_interface|Interface
section_about|Sobre
installed_models|Instalados no servidor
no_models|Ainda não há modelos instalados.
badge_default|Padrão
badge_loaded|Na memória
badge_selected|Escolhido
use_model|Usar
delete_model|Apagar
confirm_delete|Apagar {0} do servidor? Libera {1}.
add_model|Adicionar um modelo
add_model_hint|Cole o nome ou o link de um modelo do Hugging Face. Serve qualquer modelo Whisper: os do faster-whisper (CTranslate2) são usados como estão e os normais (transformers) são convertidos sozinhos. Um link direto para um .zip ou .tar.gz com um modelo também serve.
add_model_placeholder|ex.: Systran/faster-whisper-large-v3
download|Baixar
suggestions|Sugestões:
browse_hf|Ver modelos Whisper no Hugging Face
vram_hint|Modelos maiores acertam mais, mas pedem mais memória da placa de vídeo: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB.
keep_open|Deixe esta página aberta até o download terminar.
job_downloading|Baixando… {0} de {1}
job_downloading_nosize|Baixando… {0}
job_converting|Convertendo para o formato faster-whisper…
job_extracting|Descompactando…
job_ready|Instalado
job_error|Falhou: {0}
retry|Tentar de novo
plain_server_hint|É um servidor WhisperLive padrão: digite um tamanho de modelo (tiny, base, small, medium, large-v3, large-v3-turbo) e o servidor o baixa na primeira vez. Para baixar qualquer modelo por aqui, instale no servidor o complemento do Stream Transcription.
model_name|Nome do modelo
save|Salvar
saved|Salvo
reset_position|Reposicionar as legendas
position_reset_done|Pronto: elas voltarão para baixo.
section_performance|Desempenho
performance_hint|Se a placa de vídeo do servidor ficar sem memória (legendas que não chegam ou um aviso de memória), estas duas opções liberam bastante. Só funcionam com o servidor do Stream Transcription.
precision|Precisão do modelo
precision_auto|Automática
precision_int8|Economizar memória (int8)
precision_hint|int8 usa cerca de metade da memória de vídeo e, na prática, escreve o mesmo texto.
translator_device|O tradutor roda na
device_gpu|Placa de vídeo
device_cpu|Processador (CPU)
translator_device_hint|No processador libera memória de vídeo, mas as legendas traduzidas chegam um pouco mais tarde.
interface_lang|Idioma da interface
lang_auto|O do navegador
about_text|Software livre (licença MIT). O áudio só vai para o servidor que você configurar aqui; nada é enviado para nenhum outro lugar.
about_based|Baseado no WhisperLive, da Collabora.
source_code|Código-fonte
subtitle_preview|É assim que suas legendas vão ficar.
err_invalid_source|Isso não é um nome de modelo do Hugging Face nem um link.
err_unsupported_url|Só links do Hugging Face ou links diretos para arquivos .zip / .tar.gz.
err_repo_not_found|Esse modelo não existe no Hugging Face (confira o nome).
err_gated_repo|Esse modelo pede para aceitar os termos no Hugging Face; o servidor precisa de um HF_TOKEN.
err_not_whisper|Isso não é um modelo Whisper.
err_no_weights|Esse repositório não tem os pesos do modelo.
err_network_error|Erro de rede. Tente de novo: continua de onde parou.
err_download_failed|O download falhou.
err_convert_failed|Não foi possível converter o modelo.
err_bad_archive|O arquivo compactado está danificado ou não é seguro.
err_already_downloading|Já está sendo baixado.
err_already_installed|Já está instalado.
err_management_disabled|O gerenciamento de modelos está desativado neste servidor.
err_is_default|É o modelo padrão do servidor; não pode ser apagado daqui.
err_in_use|Uma transcrição em andamento está usando ele.
err_not_found|Esse modelo não está mais no servidor.
err_server_error|Erro do servidor.
err_unreachable|Não foi possível conectar ao servidor.
err_timeout|O servidor não respondeu a tempo.
err_unknown|Erro inesperado ({0}).
"""

LANGS['fr'] = """
extName|Stream Transcription
extDescription|Sous-titres en direct pour n’importe quel onglet, transcrits et traduits par votre propre serveur Whisper.
start|Activer les sous-titres
stop|Arrêter les sous-titres
status_idle|Prêt
status_connecting|Connexion…
status_loading|Chargement du modèle…
status_listening|Écoute…
status_live|En direct
status_stalled|Audio arrêté
status_error|Erreur
status_noresponse|Pas de réponse
model|Modèle
model_server_default|Celui du serveur
model_default_tag|{0} · par défaut
manage_models|Gérer les modèles
spoken_lang|Langue de l’audio
auto_detect|Automatique
detected|Détectée : {0}
subs_lang|Sous-titres en
original_lang|Sans traduction
lines|Lignes
text_size|Taille du texte
save_srt|Enregistrer les sous-titres (.srt) à l’arrêt
advanced|Avancé
use_vad|Ignorer les silences (détection de voix)
settings|Réglages
first_load_hint|La première fois, le chargement d’un modèle peut prendre jusqu’à une minute.
options_locked|Arrêtez les sous-titres pour changer ces options.
server_setup_title|Connectez votre serveur
server_setup_hint|Stream Transcription a besoin d’un serveur WhisperLive sur votre ordinateur ou votre réseau.
server_address|Adresse du serveur
server_placeholder|ex. localhost:9090 ou 192.168.1.10:9090
connect|Connecter
server_ok_models|Connecté · {0} modèles
server_ok_one_model|Connecté · 1 modèle
server_plain|Connecté · WhisperLive standard (sans gestion des modèles)
server_checking|Vérification…
server_unreachable|Impossible de joindre le serveur. Est-il allumé ? Vérifiez l’adresse et le pare-feu.
server_timeout|Le serveur n’a pas répondu à temps.
server_bad_url|Cette adresse n’est pas valide.
server_change|Modifier
server_help|Comment installer un serveur ?
server_help_1|Il vous faut un serveur WhisperLive (libre et gratuit) sur un ordinateur, idéalement avec une carte graphique NVIDIA. Les petits modèles fonctionnent aussi avec le seul processeur.
server_help_2|Saisissez ensuite son adresse ici : l’IP de l’ordinateur et le port, ex. 192.168.1.10:9090. S’il tourne sur cet ordinateur, localhost:9090.
server_help_3|Pour télécharger et gérer des modèles depuis cette page, ajoutez au serveur le module de Stream Transcription.
server_help_guide|Guide pas à pas
error_capture|Cet onglet ne peut pas être capturé (pages du navigateur, boutiques d’extensions et PDF sont exclus).
error_no_media|Il n’y a ni vidéo ni audio sur cette page.
error_server_full|Le serveur est occupé. Attente estimée : {0} min.
error_disconnected|Le serveur a fermé la connexion.
error_model_load|⚠ Pas assez de mémoire graphique (VRAM) sur le serveur pour ce modèle. Choisissez un modèle plus petit ou activez « Économiser la mémoire (int8) » dans Avancé.
warn_no_response|⚠ Les sous-titres n’arrivent plus alors qu’il y a du son. Le modèle ne tient sans doute pas dans la mémoire graphique (VRAM) du serveur : choisissez un modèle plus petit ou activez « Économiser la mémoire (int8) » dans Avancé.
warn_slow_load|⚠ Le modèle met trop de temps à charger. Il ne tient peut-être pas dans la mémoire graphique (VRAM) du serveur : choisissez un modèle plus petit ou activez « Économiser la mémoire (int8) » dans Avancé.
error_reload|Rechargez la page (F5) et recommencez.
error_no_server|Configurez d’abord le serveur.
settings_title|Stream Transcription · Réglages
section_server|Serveur
section_models|Modèles
section_subtitles|Sous-titres
section_interface|Interface
section_about|À propos
installed_models|Installés sur le serveur
no_models|Aucun modèle installé pour l’instant.
badge_default|Par défaut
badge_loaded|En mémoire
badge_selected|Choisi
use_model|Utiliser
delete_model|Supprimer
confirm_delete|Supprimer {0} du serveur ? Cela libère {1}.
add_model|Ajouter un modèle
add_model_hint|Collez le nom ou le lien d’un modèle Hugging Face. N’importe quel modèle Whisper convient : ceux de faster-whisper (CTranslate2) s’utilisent tels quels et les normaux (transformers) sont convertis automatiquement. Un lien direct vers un .zip ou .tar.gz contenant un modèle fonctionne aussi.
add_model_placeholder|ex. Systran/faster-whisper-large-v3
download|Télécharger
suggestions|Suggestions :
browse_hf|Voir les modèles Whisper sur Hugging Face
vram_hint|Les grands modèles sont plus précis mais demandent plus de mémoire graphique : small ≈ 1 Go, medium ≈ 2 Go, large ≈ 4 Go.
keep_open|Laissez cette page ouverte jusqu’à la fin du téléchargement.
job_downloading|Téléchargement… {0} sur {1}
job_downloading_nosize|Téléchargement… {0}
job_converting|Conversion au format faster-whisper…
job_extracting|Décompression…
job_ready|Installé
job_error|Échec : {0}
retry|Réessayer
plain_server_hint|C’est un serveur WhisperLive standard : saisissez une taille de modèle (tiny, base, small, medium, large-v3, large-v3-turbo) et le serveur la télécharge la première fois. Pour télécharger n’importe quel modèle d’ici, installez le module de Stream Transcription sur le serveur.
model_name|Nom du modèle
save|Enregistrer
saved|Enregistré
reset_position|Replacer les sous-titres
position_reset_done|C’est fait : ils reviendront en bas.
section_performance|Performances
performance_hint|Si la carte graphique du serveur manque de mémoire (sous-titres qui n’arrivent pas ou alerte mémoire), ces deux options en libèrent beaucoup. Elles ne marchent qu’avec le serveur de Stream Transcription.
precision|Précision du modèle
precision_auto|Automatique
precision_int8|Économiser la mémoire (int8)
precision_hint|int8 utilise environ la moitié de la mémoire graphique et, en pratique, écrit le même texte.
translator_device|Le traducteur tourne sur
device_gpu|La carte graphique
device_cpu|Le processeur (CPU)
translator_device_hint|Sur le processeur, il libère de la mémoire graphique, mais les sous-titres traduits arrivent un peu plus tard.
interface_lang|Langue de l’interface
lang_auto|Celle du navigateur
about_text|Logiciel libre (licence MIT). L’audio ne va qu’au serveur que vous configurez ici ; rien n’est envoyé ailleurs.
about_based|Basé sur WhisperLive, de Collabora.
source_code|Code source
subtitle_preview|Voici à quoi ressembleront vos sous-titres.
err_invalid_source|Ce n’est ni un nom de modèle Hugging Face ni un lien.
err_unsupported_url|Uniquement des liens Hugging Face ou des liens directs vers des fichiers .zip / .tar.gz.
err_repo_not_found|Ce modèle n’existe pas sur Hugging Face (vérifiez le nom).
err_gated_repo|Ce modèle demande d’accepter ses conditions sur Hugging Face ; le serveur a besoin d’un HF_TOKEN.
err_not_whisper|Ce n’est pas un modèle Whisper.
err_no_weights|Ce dépôt ne contient pas les poids du modèle.
err_network_error|Erreur réseau. Réessayez : cela reprend là où ça s’est arrêté.
err_download_failed|Le téléchargement a échoué.
err_convert_failed|Impossible de convertir le modèle.
err_bad_archive|L’archive est endommagée ou dangereuse.
err_already_downloading|Il est déjà en cours de téléchargement.
err_already_installed|Il est déjà installé.
err_management_disabled|La gestion des modèles est désactivée sur ce serveur.
err_is_default|C’est le modèle par défaut du serveur ; il ne peut pas être supprimé d’ici.
err_in_use|Une transcription en cours l’utilise.
err_not_found|Ce modèle n’est plus sur le serveur.
err_server_error|Erreur du serveur.
err_unreachable|Impossible de joindre le serveur.
err_timeout|Le serveur n’a pas répondu à temps.
err_unknown|Erreur inattendue ({0}).
"""

LANGS['de'] = """
extName|Stream Transcription
extDescription|Live-Untertitel für jeden Tab, transkribiert und übersetzt von deinem eigenen Whisper-Server.
start|Untertitel starten
stop|Untertitel beenden
status_idle|Bereit
status_connecting|Verbinde…
status_loading|Lade das Modell…
status_listening|Höre zu…
status_live|Live
status_stalled|Audio angehalten
status_error|Fehler
status_noresponse|Keine Antwort
model|Modell
model_server_default|Das des Servers
model_default_tag|{0} · Standard
manage_models|Modelle verwalten
spoken_lang|Sprache des Audios
auto_detect|Automatisch
detected|Erkannt: {0}
subs_lang|Untertitel auf
original_lang|Ohne Übersetzung
lines|Zeilen
text_size|Textgröße
save_srt|Untertitel (.srt) beim Beenden speichern
advanced|Erweitert
use_vad|Stille überspringen (Spracherkennung)
settings|Einstellungen
first_load_hint|Beim ersten Mal kann das Laden eines Modells bis zu einer Minute dauern.
options_locked|Beende die Untertitel, um diese Optionen zu ändern.
server_setup_title|Verbinde deinen Server
server_setup_hint|Stream Transcription braucht einen WhisperLive-Server auf deinem Computer oder in deinem Netzwerk.
server_address|Serveradresse
server_placeholder|z. B. localhost:9090 oder 192.168.1.10:9090
connect|Verbinden
server_ok_models|Verbunden · {0} Modelle
server_ok_one_model|Verbunden · 1 Modell
server_plain|Verbunden · Standard-WhisperLive (ohne Modellverwaltung)
server_checking|Prüfe…
server_unreachable|Der Server ist nicht erreichbar. Läuft er? Prüfe die Adresse und die Firewall.
server_timeout|Der Server hat nicht rechtzeitig geantwortet.
server_bad_url|Diese Adresse ist ungültig.
server_change|Ändern
server_help|Wie richte ich einen Server ein?
server_help_1|Du brauchst einen WhisperLive-Server (frei und kostenlos) auf einem Computer, am besten mit einer NVIDIA-Grafikkarte. Kleine Modelle laufen auch nur auf dem Prozessor.
server_help_2|Gib dann hier seine Adresse ein: die IP des Computers und den Port, z. B. 192.168.1.10:9090. Läuft er auf diesem Computer, localhost:9090.
server_help_3|Um Modelle von dieser Seite aus herunterzuladen und zu verwalten, füge dem Server das Stream-Transcription-Add-on hinzu.
server_help_guide|Schritt-für-Schritt-Anleitung
error_capture|Dieser Tab lässt sich nicht aufnehmen (Browserseiten, Erweiterungsshops und PDFs sind gesperrt).
error_no_media|Auf dieser Seite gibt es weder Video noch Audio.
error_server_full|Der Server ist ausgelastet. Geschätzte Wartezeit: {0} min.
error_disconnected|Der Server hat die Verbindung geschlossen.
error_model_load|⚠ Auf dem Server reicht der Grafikspeicher (VRAM) für dieses Modell nicht. Wähle ein kleineres Modell oder schalte unter Erweitert „Speicher sparen (int8)“ ein.
warn_no_response|⚠ Es kommen keine Untertitel mehr, obwohl Ton da ist. Wahrscheinlich passt das Modell nicht in den Grafikspeicher (VRAM) des Servers: Wähle ein kleineres Modell oder schalte unter Erweitert „Speicher sparen (int8)“ ein.
warn_slow_load|⚠ Das Modell lädt zu lange. Vielleicht passt es nicht in den Grafikspeicher (VRAM) des Servers: Wähle ein kleineres Modell oder schalte unter Erweitert „Speicher sparen (int8)“ ein.
error_reload|Lade die Seite neu (F5) und starte erneut.
error_no_server|Richte zuerst den Server ein.
settings_title|Stream Transcription · Einstellungen
section_server|Server
section_models|Modelle
section_subtitles|Untertitel
section_interface|Oberfläche
section_about|Über
installed_models|Auf dem Server installiert
no_models|Noch keine Modelle installiert.
badge_default|Standard
badge_loaded|Im Speicher
badge_selected|Ausgewählt
use_model|Verwenden
delete_model|Löschen
confirm_delete|{0} vom Server löschen? Das gibt {1} frei.
add_model|Ein Modell hinzufügen
add_model_hint|Füge den Namen oder den Link eines Modells von Hugging Face ein. Jedes Whisper-Modell geht: faster-whisper-Modelle (CTranslate2) werden direkt genutzt, normale (transformers) werden automatisch umgewandelt. Ein direkter Link auf ein .zip oder .tar.gz mit einem Modell geht auch.
add_model_placeholder|z. B. Systran/faster-whisper-large-v3
download|Herunterladen
suggestions|Vorschläge:
browse_hf|Whisper-Modelle auf Hugging Face ansehen
vram_hint|Größere Modelle sind genauer, brauchen aber mehr Grafikspeicher: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB.
keep_open|Lass diese Seite offen, bis der Download fertig ist.
job_downloading|Lade herunter… {0} von {1}
job_downloading_nosize|Lade herunter… {0}
job_converting|Wandle ins faster-whisper-Format um…
job_extracting|Entpacke…
job_ready|Installiert
job_error|Fehlgeschlagen: {0}
retry|Erneut versuchen
plain_server_hint|Das ist ein Standard-WhisperLive-Server: Gib eine Modellgröße ein (tiny, base, small, medium, large-v3, large-v3-turbo), der Server lädt sie beim ersten Mal herunter. Um beliebige Modelle von hier herunterzuladen, installiere das Stream-Transcription-Add-on auf dem Server.
model_name|Modellname
save|Speichern
saved|Gespeichert
reset_position|Untertitelposition zurücksetzen
position_reset_done|Erledigt: Sie wandern wieder nach unten.
section_performance|Leistung
performance_hint|Wenn der Grafikkarte des Servers der Speicher ausgeht (Untertitel kommen nicht an oder eine Speicherwarnung erscheint), geben diese beiden Optionen viel frei. Sie funktionieren nur mit dem Stream-Transcription-Server.
precision|Modellgenauigkeit
precision_auto|Automatisch
precision_int8|Speicher sparen (int8)
precision_hint|int8 braucht etwa halb so viel Grafikspeicher und schreibt in der Praxis denselben Text.
translator_device|Der Übersetzer läuft auf
device_gpu|Grafikkarte
device_cpu|Prozessor (CPU)
translator_device_hint|Auf dem Prozessor wird Grafikspeicher frei, aber übersetzte Untertitel kommen etwas später.
interface_lang|Sprache der Oberfläche
lang_auto|Wie der Browser
about_text|Freie Software (MIT-Lizenz). Das Audio geht nur an den Server, den du hier einrichtest; nichts wird woandershin geschickt.
about_based|Basiert auf WhisperLive von Collabora.
source_code|Quellcode
subtitle_preview|So sehen deine Untertitel aus.
err_invalid_source|Das ist weder ein Hugging-Face-Modellname noch ein Link.
err_unsupported_url|Nur Hugging-Face-Links oder direkte Links auf .zip-/.tar.gz-Dateien.
err_repo_not_found|Dieses Modell gibt es auf Hugging Face nicht (prüfe den Namen).
err_gated_repo|Für dieses Modell müssen auf Hugging Face Bedingungen akzeptiert werden; der Server braucht ein HF_TOKEN.
err_not_whisper|Das ist kein Whisper-Modell.
err_no_weights|Dieses Repository enthält keine Modellgewichte.
err_network_error|Netzwerkfehler. Versuch es noch mal: Es geht dort weiter, wo es aufgehört hat.
err_download_failed|Der Download ist fehlgeschlagen.
err_convert_failed|Das Modell konnte nicht umgewandelt werden.
err_bad_archive|Das Archiv ist beschädigt oder unsicher.
err_already_downloading|Es wird schon heruntergeladen.
err_already_installed|Es ist schon installiert.
err_management_disabled|Die Modellverwaltung ist auf diesem Server ausgeschaltet.
err_is_default|Das ist das Standardmodell des Servers; es kann hier nicht gelöscht werden.
err_in_use|Eine laufende Transkription verwendet es.
err_not_found|Dieses Modell ist nicht mehr auf dem Server.
err_server_error|Serverfehler.
err_unreachable|Der Server ist nicht erreichbar.
err_timeout|Der Server hat nicht rechtzeitig geantwortet.
err_unknown|Unerwarteter Fehler ({0}).
"""

LANGS['it'] = """
extName|Stream Transcription
extDescription|Sottotitoli in diretta per qualsiasi scheda, trascritti e tradotti dal tuo server Whisper.
start|Attiva sottotitoli
stop|Disattiva sottotitoli
status_idle|Pronto
status_connecting|Connessione…
status_loading|Caricamento del modello…
status_listening|In ascolto…
status_live|In diretta
status_stalled|Audio fermo
status_error|Errore
status_noresponse|Nessuna risposta
model|Modello
model_server_default|Quello del server
model_default_tag|{0} · predefinito
manage_models|Gestisci modelli
spoken_lang|Lingua dell’audio
auto_detect|Automatico
detected|Rilevata: {0}
subs_lang|Sottotitoli in
original_lang|Senza traduzione
lines|Righe
text_size|Dimensione del testo
save_srt|Salva i sottotitoli (.srt) quando ti fermi
advanced|Avanzate
use_vad|Salta i silenzi (rilevamento della voce)
settings|Impostazioni
first_load_hint|La prima volta il caricamento di un modello può richiedere fino a un minuto.
options_locked|Disattiva i sottotitoli per cambiare queste opzioni.
server_setup_title|Collega il tuo server
server_setup_hint|Stream Transcription ha bisogno di un server WhisperLive sul tuo computer o nella tua rete.
server_address|Indirizzo del server
server_placeholder|es. localhost:9090 o 192.168.1.10:9090
connect|Collega
server_ok_models|Collegato · {0} modelli
server_ok_one_model|Collegato · 1 modello
server_plain|Collegato · WhisperLive standard (senza gestione dei modelli)
server_checking|Verifica…
server_unreachable|Impossibile raggiungere il server. È acceso? Controlla l’indirizzo e il firewall.
server_timeout|Il server non ha risposto in tempo.
server_bad_url|Questo indirizzo non è valido.
server_change|Cambia
server_help|Come configuro un server?
server_help_1|Ti serve un server WhisperLive (libero e gratuito) su un computer, meglio se con una scheda grafica NVIDIA. I modelli piccoli funzionano anche solo con il processore.
server_help_2|Poi scrivi qui il suo indirizzo: l’IP del computer e la porta, es. 192.168.1.10:9090. Se è su questo stesso computer, localhost:9090.
server_help_3|Per scaricare e gestire i modelli da questa pagina, aggiungi al server il componente di Stream Transcription.
server_help_guide|Guida passo passo
error_capture|Questa scheda non si può catturare (pagine del browser, negozi di estensioni e PDF sono esclusi).
error_no_media|In questa pagina non ci sono video né audio.
error_server_full|Il server è occupato. Attesa stimata: {0} min.
error_disconnected|Il server ha chiuso la connessione.
error_model_load|⚠ Il server non ha abbastanza memoria grafica (VRAM) per questo modello. Scegli un modello più piccolo o attiva “Risparmia memoria (int8)” in Avanzate.
warn_no_response|⚠ I sottotitoli non arrivano più anche se c’è audio. Probabilmente il modello non entra nella memoria grafica (VRAM) del server: scegli un modello più piccolo o attiva “Risparmia memoria (int8)” in Avanzate.
warn_slow_load|⚠ Il modello ci mette troppo a caricarsi. Forse non entra nella memoria grafica (VRAM) del server: scegli un modello più piccolo o attiva “Risparmia memoria (int8)” in Avanzate.
error_reload|Ricarica la pagina (F5) e ricomincia.
error_no_server|Prima configura il server.
settings_title|Stream Transcription · Impostazioni
section_server|Server
section_models|Modelli
section_subtitles|Sottotitoli
section_interface|Interfaccia
section_about|Informazioni
installed_models|Installati sul server
no_models|Ancora nessun modello installato.
badge_default|Predefinito
badge_loaded|In memoria
badge_selected|Scelto
use_model|Usa
delete_model|Elimina
confirm_delete|Eliminare {0} dal server? Libera {1}.
add_model|Aggiungi un modello
add_model_hint|Incolla il nome o il link di un modello di Hugging Face. Va bene qualsiasi modello Whisper: quelli di faster-whisper (CTranslate2) si usano così come sono e quelli normali (transformers) vengono convertiti da soli. Va bene anche un link diretto a un .zip o .tar.gz con un modello.
add_model_placeholder|es. Systran/faster-whisper-large-v3
download|Scarica
suggestions|Suggerimenti:
browse_hf|Vedi i modelli Whisper su Hugging Face
vram_hint|I modelli grandi sono più precisi ma chiedono più memoria della scheda grafica: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB.
keep_open|Lascia aperta questa pagina finché il download non finisce.
job_downloading|Scaricamento… {0} di {1}
job_downloading_nosize|Scaricamento… {0}
job_converting|Conversione nel formato faster-whisper…
job_extracting|Estrazione…
job_ready|Installato
job_error|Non riuscito: {0}
retry|Riprova
plain_server_hint|È un server WhisperLive standard: scrivi una dimensione di modello (tiny, base, small, medium, large-v3, large-v3-turbo) e il server la scarica la prima volta. Per scaricare qualsiasi modello da qui, installa sul server il componente di Stream Transcription.
model_name|Nome del modello
save|Salva
saved|Salvato
reset_position|Riposiziona i sottotitoli
position_reset_done|Fatto: torneranno in basso.
section_performance|Prestazioni
performance_hint|Se la scheda grafica del server resta senza memoria (sottotitoli che non arrivano o un avviso di memoria), queste due opzioni ne liberano parecchia. Funzionano solo con il server di Stream Transcription.
precision|Precisione del modello
precision_auto|Automatica
precision_int8|Risparmia memoria (int8)
precision_hint|int8 usa circa metà della memoria grafica e, in pratica, scrive lo stesso testo.
translator_device|Il traduttore gira su
device_gpu|Scheda grafica
device_cpu|Processore (CPU)
translator_device_hint|Sul processore libera memoria grafica, ma i sottotitoli tradotti arrivano un po’ dopo.
interface_lang|Lingua dell’interfaccia
lang_auto|Quella del browser
about_text|Software libero (licenza MIT). L’audio va solo al server che configuri qui; non viene inviato altrove.
about_based|Basato su WhisperLive di Collabora.
source_code|Codice sorgente
subtitle_preview|Ecco come appariranno i tuoi sottotitoli.
err_invalid_source|Non è un nome di modello di Hugging Face né un link.
err_unsupported_url|Solo link di Hugging Face o link diretti a file .zip / .tar.gz.
err_repo_not_found|Quel modello non esiste su Hugging Face (controlla il nome).
err_gated_repo|Quel modello chiede di accettare le sue condizioni su Hugging Face; il server ha bisogno di un HF_TOKEN.
err_not_whisper|Non è un modello Whisper.
err_no_weights|Quel repository non ha i pesi del modello.
err_network_error|Errore di rete. Riprova: riparte da dove si era fermato.
err_download_failed|Il download non è riuscito.
err_convert_failed|Non è stato possibile convertire il modello.
err_bad_archive|L’archivio è danneggiato o non è sicuro.
err_already_downloading|Lo sta già scaricando.
err_already_installed|È già installato.
err_management_disabled|La gestione dei modelli è disattivata su questo server.
err_is_default|È il modello predefinito del server; non si può eliminare da qui.
err_in_use|Lo sta usando una trascrizione in corso.
err_not_found|Quel modello non è più sul server.
err_server_error|Errore del server.
err_unreachable|Impossibile raggiungere il server.
err_timeout|Il server non ha risposto in tempo.
err_unknown|Errore imprevisto ({0}).
"""

LANGS['nl'] = """
extName|Stream Transcription
extDescription|Live-ondertitels voor elk tabblad, getranscribeerd en vertaald door je eigen Whisper-server.
start|Ondertitels aan
stop|Ondertitels uit
status_idle|Klaar
status_connecting|Verbinden…
status_loading|Model laden…
status_listening|Luisteren…
status_live|Live
status_stalled|Audio gestopt
status_error|Fout
status_noresponse|Geen antwoord
model|Model
model_server_default|Dat van de server
model_default_tag|{0} · standaard
manage_models|Modellen beheren
spoken_lang|Taal van de audio
auto_detect|Automatisch
detected|Herkend: {0}
subs_lang|Ondertitels in
original_lang|Geen vertaling
lines|Regels
text_size|Tekstgrootte
save_srt|Ondertitels (.srt) opslaan bij het stoppen
advanced|Geavanceerd
use_vad|Stiltes overslaan (stemdetectie)
settings|Instellingen
first_load_hint|De eerste keer kan het laden van een model tot een minuut duren.
options_locked|Zet de ondertitels uit om deze opties te wijzigen.
server_setup_title|Verbind je server
server_setup_hint|Stream Transcription heeft een WhisperLive-server op je computer of in je netwerk nodig.
server_address|Serveradres
server_placeholder|bijv. localhost:9090 of 192.168.1.10:9090
connect|Verbinden
server_ok_models|Verbonden · {0} modellen
server_ok_one_model|Verbonden · 1 model
server_plain|Verbonden · standaard WhisperLive (zonder modelbeheer)
server_checking|Controleren…
server_unreachable|De server is niet bereikbaar. Staat hij aan? Controleer het adres en de firewall.
server_timeout|De server antwoordde niet op tijd.
server_bad_url|Dat adres is ongeldig.
server_change|Wijzigen
server_help|Hoe zet ik een server op?
server_help_1|Je hebt een WhisperLive-server nodig (vrij en gratis) op een computer, liefst met een NVIDIA-videokaart. Kleine modellen werken ook alleen op de processor.
server_help_2|Typ hier daarna zijn adres: het IP van de computer en de poort, bijv. 192.168.1.10:9090. Draait hij op deze computer, dan localhost:9090.
server_help_3|Om vanaf deze pagina modellen te downloaden en te beheren, voeg je de Stream Transcription-add-on toe aan de server.
server_help_guide|Stapsgewijze handleiding
error_capture|Dit tabblad kan niet worden opgenomen (browserpagina’s, extensiewinkels en pdf’s zijn uitgesloten).
error_no_media|Er staat geen video of audio op deze pagina.
error_server_full|De server is bezet. Geschatte wachttijd: {0} min.
error_disconnected|De server heeft de verbinding gesloten.
error_model_load|⚠ Er is te weinig grafisch geheugen (VRAM) op de server voor dit model. Kies een kleiner model of zet ‘Geheugen besparen (int8)’ aan bij Geavanceerd.
warn_no_response|⚠ Er komen geen ondertitels meer, al is er geluid. Waarschijnlijk past het model niet in het grafische geheugen (VRAM) van de server: kies een kleiner model of zet ‘Geheugen besparen (int8)’ aan bij Geavanceerd.
warn_slow_load|⚠ Het laden van het model duurt te lang. Misschien past het niet in het grafische geheugen (VRAM) van de server: kies een kleiner model of zet ‘Geheugen besparen (int8)’ aan bij Geavanceerd.
error_reload|Herlaad de pagina (F5) en begin opnieuw.
error_no_server|Stel eerst de server in.
settings_title|Stream Transcription · Instellingen
section_server|Server
section_models|Modellen
section_subtitles|Ondertitels
section_interface|Interface
section_about|Over
installed_models|Geïnstalleerd op de server
no_models|Nog geen modellen geïnstalleerd.
badge_default|Standaard
badge_loaded|In geheugen
badge_selected|Gekozen
use_model|Gebruiken
delete_model|Verwijderen
confirm_delete|{0} van de server verwijderen? Dat maakt {1} vrij.
add_model|Een model toevoegen
add_model_hint|Plak de naam of de link van een model op Hugging Face. Elk Whisper-model werkt: faster-whisper-modellen (CTranslate2) worden zo gebruikt en gewone (transformers) automatisch omgezet. Een directe link naar een .zip of .tar.gz met een model werkt ook.
add_model_placeholder|bijv. Systran/faster-whisper-large-v3
download|Downloaden
suggestions|Suggesties:
browse_hf|Whisper-modellen op Hugging Face bekijken
vram_hint|Grotere modellen zijn nauwkeuriger maar vragen meer videogeheugen: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB.
keep_open|Laat deze pagina open tot de download klaar is.
job_downloading|Downloaden… {0} van {1}
job_downloading_nosize|Downloaden… {0}
job_converting|Omzetten naar het faster-whisper-formaat…
job_extracting|Uitpakken…
job_ready|Geïnstalleerd
job_error|Mislukt: {0}
retry|Opnieuw
plain_server_hint|Dit is een standaard WhisperLive-server: typ een modelgrootte (tiny, base, small, medium, large-v3, large-v3-turbo) en de server downloadt die de eerste keer. Om elk model vanaf hier te downloaden, installeer je de Stream Transcription-add-on op de server.
model_name|Modelnaam
save|Opslaan
saved|Opgeslagen
reset_position|Positie van ondertitels herstellen
position_reset_done|Klaar: ze gaan weer naar onderen.
section_performance|Prestaties
performance_hint|Als de videokaart van de server zonder geheugen komt (ondertitels die niet komen of een geheugenwaarschuwing), maken deze twee opties veel vrij. Ze werken alleen met de Stream Transcription-server.
precision|Modelprecisie
precision_auto|Automatisch
precision_int8|Geheugen besparen (int8)
precision_hint|int8 gebruikt ongeveer de helft van het videogeheugen en schrijft in de praktijk dezelfde tekst.
translator_device|De vertaler draait op
device_gpu|Videokaart
device_cpu|Processor (CPU)
translator_device_hint|Op de processor komt videogeheugen vrij, maar vertaalde ondertitels komen iets later.
interface_lang|Taal van de interface
lang_auto|Die van de browser
about_text|Vrije software (MIT-licentie). De audio gaat alleen naar de server die je hier instelt; er wordt niets ergens anders heen gestuurd.
about_based|Gebaseerd op WhisperLive van Collabora.
source_code|Broncode
subtitle_preview|Zo zien je ondertitels eruit.
err_invalid_source|Dat is geen modelnaam van Hugging Face en geen link.
err_unsupported_url|Alleen links van Hugging Face of directe links naar .zip-/.tar.gz-bestanden.
err_repo_not_found|Dat model bestaat niet op Hugging Face (controleer de naam).
err_gated_repo|Voor dat model moet je de voorwaarden op Hugging Face accepteren; de server heeft een HF_TOKEN nodig.
err_not_whisper|Dat is geen Whisper-model.
err_no_weights|Die repository bevat geen modelgewichten.
err_network_error|Netwerkfout. Probeer opnieuw: het gaat verder waar het stopte.
err_download_failed|De download is mislukt.
err_convert_failed|Het model kon niet worden omgezet.
err_bad_archive|Het archief is beschadigd of onveilig.
err_already_downloading|Het wordt al gedownload.
err_already_installed|Het is al geïnstalleerd.
err_management_disabled|Modelbeheer staat uit op deze server.
err_is_default|Dat is het standaardmodel van de server; het kan hier niet worden verwijderd.
err_in_use|Een lopende transcriptie gebruikt het.
err_not_found|Dat model staat niet meer op de server.
err_server_error|Serverfout.
err_unreachable|De server is niet bereikbaar.
err_timeout|De server antwoordde niet op tijd.
err_unknown|Onverwachte fout ({0}).
"""

LANGS['pl'] = """
extName|Stream Transcription
extDescription|Napisy na żywo w dowolnej karcie, transkrybowane i tłumaczone przez twój własny serwer Whisper.
start|Włącz napisy
stop|Wyłącz napisy
status_idle|Gotowe
status_connecting|Łączenie…
status_loading|Wczytywanie modelu…
status_listening|Nasłuchiwanie…
status_live|Na żywo
status_stalled|Dźwięk zatrzymany
status_error|Błąd
status_noresponse|Brak odpowiedzi
model|Model
model_server_default|Domyślny serwera
model_default_tag|{0} · domyślny
manage_models|Zarządzaj modelami
spoken_lang|Język dźwięku
auto_detect|Automatycznie
detected|Wykryto: {0}
subs_lang|Napisy w języku
original_lang|Bez tłumaczenia
lines|Wiersze
text_size|Rozmiar tekstu
save_srt|Zapisz napisy (.srt) po zatrzymaniu
advanced|Zaawansowane
use_vad|Pomijaj ciszę (wykrywanie mowy)
settings|Ustawienia
first_load_hint|Za pierwszym razem wczytanie modelu może potrwać do minuty.
options_locked|Wyłącz napisy, aby zmienić te opcje.
server_setup_title|Połącz swój serwer
server_setup_hint|Stream Transcription potrzebuje serwera WhisperLive na twoim komputerze lub w twojej sieci.
server_address|Adres serwera
server_placeholder|np. localhost:9090 lub 192.168.1.10:9090
connect|Połącz
server_ok_models|Połączono · modele: {0}
server_ok_one_model|Połączono · 1 model
server_plain|Połączono · standardowy WhisperLive (bez zarządzania modelami)
server_checking|Sprawdzanie…
server_unreachable|Nie można połączyć się z serwerem. Czy jest włączony? Sprawdź adres i zaporę.
server_timeout|Serwer nie odpowiedział na czas.
server_bad_url|Ten adres jest nieprawidłowy.
server_change|Zmień
server_help|Jak skonfigurować serwer?
server_help_1|Potrzebujesz serwera WhisperLive (wolnego i darmowego) na komputerze, najlepiej z kartą graficzną NVIDIA. Małe modele działają też na samym procesorze.
server_help_2|Potem wpisz tu jego adres: IP komputera i port, np. 192.168.1.10:9090. Jeśli działa na tym komputerze — localhost:9090.
server_help_3|Aby pobierać modele i zarządzać nimi z tej strony, dodaj do serwera dodatek Stream Transcription.
server_help_guide|Przewodnik krok po kroku
error_capture|Tej karty nie można przechwycić (strony przeglądarki, sklepy z rozszerzeniami i pliki PDF są wykluczone).
error_no_media|Na tej stronie nie ma wideo ani dźwięku.
error_server_full|Serwer jest zajęty. Szacowany czas oczekiwania: {0} min.
error_disconnected|Serwer zamknął połączenie.
error_model_load|⚠ Serwer ma za mało pamięci graficznej (VRAM) na ten model. Wybierz mniejszy model lub włącz „Oszczędzaj pamięć (int8)” w Zaawansowanych.
warn_no_response|⚠ Napisy przestały przychodzić, choć jest dźwięk. Model pewnie nie mieści się w pamięci graficznej (VRAM) serwera: wybierz mniejszy model lub włącz „Oszczędzaj pamięć (int8)” w Zaawansowanych.
warn_slow_load|⚠ Model wczytuje się za długo. Może nie mieścić się w pamięci graficznej (VRAM) serwera: wybierz mniejszy model lub włącz „Oszczędzaj pamięć (int8)” w Zaawansowanych.
error_reload|Odśwież stronę (F5) i zacznij od nowa.
error_no_server|Najpierw skonfiguruj serwer.
settings_title|Stream Transcription · Ustawienia
section_server|Serwer
section_models|Modele
section_subtitles|Napisy
section_interface|Interfejs
section_about|Informacje
installed_models|Zainstalowane na serwerze
no_models|Nie ma jeszcze zainstalowanych modeli.
badge_default|Domyślny
badge_loaded|W pamięci
badge_selected|Wybrany
use_model|Użyj
delete_model|Usuń
confirm_delete|Usunąć {0} z serwera? Zwolni to {1}.
add_model|Dodaj model
add_model_hint|Wklej nazwę lub link modelu z Hugging Face. Pasuje każdy model Whisper: modele faster-whisper (CTranslate2) są używane bez zmian, a zwykłe (transformers) konwertowane automatycznie. Działa też bezpośredni link do pliku .zip lub .tar.gz z modelem.
add_model_placeholder|np. Systran/faster-whisper-large-v3
download|Pobierz
suggestions|Propozycje:
browse_hf|Zobacz modele Whisper na Hugging Face
vram_hint|Większe modele są dokładniejsze, ale potrzebują więcej pamięci karty graficznej: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB.
keep_open|Nie zamykaj tej strony, dopóki pobieranie się nie skończy.
job_downloading|Pobieranie… {0} z {1}
job_downloading_nosize|Pobieranie… {0}
job_converting|Konwersja do formatu faster-whisper…
job_extracting|Rozpakowywanie…
job_ready|Zainstalowano
job_error|Niepowodzenie: {0}
retry|Spróbuj ponownie
plain_server_hint|To standardowy serwer WhisperLive: wpisz rozmiar modelu (tiny, base, small, medium, large-v3, large-v3-turbo), a serwer pobierze go za pierwszym razem. Aby pobierać stąd dowolne modele, zainstaluj na serwerze dodatek Stream Transcription.
model_name|Nazwa modelu
save|Zapisz
saved|Zapisano
reset_position|Przywróć położenie napisów
position_reset_done|Gotowe: wrócą na dół.
section_performance|Wydajność
performance_hint|Jeśli karcie graficznej serwera brakuje pamięci (napisy nie przychodzą albo pojawia się ostrzeżenie o pamięci), te dwie opcje sporo jej zwalniają. Działają tylko z serwerem Stream Transcription.
precision|Precyzja modelu
precision_auto|Automatyczna
precision_int8|Oszczędzaj pamięć (int8)
precision_hint|int8 zużywa mniej więcej połowę pamięci graficznej i w praktyce pisze ten sam tekst.
translator_device|Tłumacz działa na
device_gpu|Karcie graficznej
device_cpu|Procesorze (CPU)
translator_device_hint|Na procesorze zwalnia pamięć graficzną, ale przetłumaczone napisy przychodzą nieco później.
interface_lang|Język interfejsu
lang_auto|Jak w przeglądarce
about_text|Wolne oprogramowanie (licencja MIT). Dźwięk trafia tylko do serwera, który tu skonfigurujesz; nic nie jest wysyłane nigdzie indziej.
about_based|Oparte na WhisperLive od Collabora.
source_code|Kod źródłowy
subtitle_preview|Tak będą wyglądać twoje napisy.
err_invalid_source|To nie jest nazwa modelu z Hugging Face ani link.
err_unsupported_url|Tylko linki do Hugging Face lub bezpośrednie linki do plików .zip / .tar.gz.
err_repo_not_found|Taki model nie istnieje na Hugging Face (sprawdź nazwę).
err_gated_repo|Ten model wymaga zaakceptowania warunków na Hugging Face; serwer potrzebuje HF_TOKEN.
err_not_whisper|To nie jest model Whisper.
err_no_weights|To repozytorium nie zawiera wag modelu.
err_network_error|Błąd sieci. Spróbuj ponownie: zacznie od miejsca, w którym przerwał.
err_download_failed|Pobieranie nie powiodło się.
err_convert_failed|Nie udało się przekonwertować modelu.
err_bad_archive|Archiwum jest uszkodzone lub niebezpieczne.
err_already_downloading|Już się pobiera.
err_already_installed|Już jest zainstalowany.
err_management_disabled|Zarządzanie modelami jest wyłączone na tym serwerze.
err_is_default|To domyślny model serwera; nie można go stąd usunąć.
err_in_use|Używa go trwająca transkrypcja.
err_not_found|Tego modelu nie ma już na serwerze.
err_server_error|Błąd serwera.
err_unreachable|Nie można połączyć się z serwerem.
err_timeout|Serwer nie odpowiedział na czas.
err_unknown|Nieoczekiwany błąd ({0}).
"""

LANGS['ru'] = """
extName|Stream Transcription
extDescription|Субтитры в реальном времени для любой вкладки: распознаёт и переводит ваш собственный сервер Whisper.
start|Включить субтитры
stop|Выключить субтитры
status_idle|Готово
status_connecting|Подключение…
status_loading|Загрузка модели…
status_listening|Слушаю…
status_live|В эфире
status_stalled|Звук остановлен
status_error|Ошибка
status_noresponse|Нет ответа
model|Модель
model_server_default|Как на сервере
model_default_tag|{0} · по умолчанию
manage_models|Управлять моделями
spoken_lang|Язык аудио
auto_detect|Автоматически
detected|Определён: {0}
subs_lang|Субтитры на
original_lang|Без перевода
lines|Строки
text_size|Размер текста
save_srt|Сохранять субтитры (.srt) при остановке
advanced|Дополнительно
use_vad|Пропускать тишину (обнаружение речи)
settings|Настройки
first_load_hint|В первый раз загрузка модели может занять до минуты.
options_locked|Выключите субтитры, чтобы изменить эти параметры.
server_setup_title|Подключите свой сервер
server_setup_hint|Stream Transcription нужен сервер WhisperLive на вашем компьютере или в вашей сети.
server_address|Адрес сервера
server_placeholder|напр. localhost:9090 или 192.168.1.10:9090
connect|Подключить
server_ok_models|Подключено · моделей: {0}
server_ok_one_model|Подключено · 1 модель
server_plain|Подключено · стандартный WhisperLive (без управления моделями)
server_checking|Проверка…
server_unreachable|Не удаётся связаться с сервером. Он включён? Проверьте адрес и брандмауэр.
server_timeout|Сервер не ответил вовремя.
server_bad_url|Этот адрес недействителен.
server_change|Изменить
server_help|Как настроить сервер?
server_help_1|Нужен сервер WhisperLive (свободный и бесплатный) на компьютере, лучше с видеокартой NVIDIA. Небольшие модели работают и на одном процессоре.
server_help_2|Затем введите здесь его адрес: IP компьютера и порт, напр. 192.168.1.10:9090. Если он на этом же компьютере — localhost:9090.
server_help_3|Чтобы скачивать модели и управлять ими с этой страницы, добавьте на сервер дополнение Stream Transcription.
server_help_guide|Пошаговое руководство
error_capture|Эту вкладку нельзя захватить (страницы браузера, магазины расширений и PDF недоступны).
error_no_media|На этой странице нет ни видео, ни звука.
error_server_full|Сервер занят. Примерное ожидание: {0} мин.
error_disconnected|Сервер закрыл соединение.
error_model_load|⚠ На сервере не хватает видеопамяти (VRAM) для этой модели. Выберите модель поменьше или включите «Экономить память (int8)» в разделе «Дополнительно».
warn_no_response|⚠ Субтитры перестали приходить, хотя звук есть. Вероятно, модель не помещается в видеопамять (VRAM) сервера: выберите модель поменьше или включите «Экономить память (int8)» в разделе «Дополнительно».
warn_slow_load|⚠ Модель загружается слишком долго. Возможно, она не помещается в видеопамять (VRAM) сервера: выберите модель поменьше или включите «Экономить память (int8)» в разделе «Дополнительно».
error_reload|Перезагрузите страницу (F5) и начните заново.
error_no_server|Сначала настройте сервер.
settings_title|Stream Transcription · Настройки
section_server|Сервер
section_models|Модели
section_subtitles|Субтитры
section_interface|Интерфейс
section_about|О программе
installed_models|Установлены на сервере
no_models|Моделей пока нет.
badge_default|По умолчанию
badge_loaded|В памяти
badge_selected|Выбрана
use_model|Использовать
delete_model|Удалить
confirm_delete|Удалить {0} с сервера? Освободится {1}.
add_model|Добавить модель
add_model_hint|Вставьте название или ссылку на модель с Hugging Face. Подойдёт любая модель Whisper: модели faster-whisper (CTranslate2) используются как есть, обычные (transformers) конвертируются автоматически. Подойдёт и прямая ссылка на .zip или .tar.gz с моделью.
add_model_placeholder|напр. Systran/faster-whisper-large-v3
download|Скачать
suggestions|Варианты:
browse_hf|Смотреть модели Whisper на Hugging Face
vram_hint|Большие модели точнее, но им нужно больше видеопамяти: small ≈ 1 ГБ, medium ≈ 2 ГБ, large ≈ 4 ГБ.
keep_open|Не закрывайте эту страницу, пока скачивание не закончится.
job_downloading|Скачивание… {0} из {1}
job_downloading_nosize|Скачивание… {0}
job_converting|Конвертация в формат faster-whisper…
job_extracting|Распаковка…
job_ready|Установлена
job_error|Не удалось: {0}
retry|Повторить
plain_server_hint|Это стандартный сервер WhisperLive: введите размер модели (tiny, base, small, medium, large-v3, large-v3-turbo), и сервер скачает её при первом запуске. Чтобы скачивать отсюда любые модели, установите на сервер дополнение Stream Transcription.
model_name|Название модели
save|Сохранить
saved|Сохранено
reset_position|Сбросить положение субтитров
position_reset_done|Готово: они вернутся вниз.
section_performance|Производительность
performance_hint|Если видеокарте сервера не хватает памяти (субтитры не приходят или появляется предупреждение о памяти), эти два параметра освобождают немало. Работают только с сервером Stream Transcription.
precision|Точность модели
precision_auto|Автоматически
precision_int8|Экономить память (int8)
precision_hint|int8 занимает примерно половину видеопамяти и на практике пишет тот же текст.
translator_device|Переводчик работает на
device_gpu|Видеокарте
device_cpu|Процессоре (CPU)
translator_device_hint|На процессоре освобождается видеопамять, но переведённые субтитры приходят чуть позже.
interface_lang|Язык интерфейса
lang_auto|Как в браузере
about_text|Свободное ПО (лицензия MIT). Звук идёт только на сервер, который вы здесь укажете; больше никуда ничего не отправляется.
about_based|Основано на WhisperLive от Collabora.
source_code|Исходный код
subtitle_preview|Так будут выглядеть ваши субтитры.
err_invalid_source|Это не название модели Hugging Face и не ссылка.
err_unsupported_url|Только ссылки на Hugging Face или прямые ссылки на файлы .zip / .tar.gz.
err_repo_not_found|Такой модели на Hugging Face нет (проверьте название).
err_gated_repo|Для этой модели нужно принять условия на Hugging Face; серверу нужен HF_TOKEN.
err_not_whisper|Это не модель Whisper.
err_no_weights|В этом репозитории нет весов модели.
err_network_error|Ошибка сети. Повторите: продолжит с того места, где остановилось.
err_download_failed|Скачивание не удалось.
err_convert_failed|Не удалось конвертировать модель.
err_bad_archive|Архив повреждён или небезопасен.
err_already_downloading|Уже скачивается.
err_already_installed|Уже установлена.
err_management_disabled|Управление моделями на этом сервере выключено.
err_is_default|Это модель сервера по умолчанию; удалить её отсюда нельзя.
err_in_use|Её использует идущая транскрипция.
err_not_found|Этой модели на сервере больше нет.
err_server_error|Ошибка сервера.
err_unreachable|Не удаётся связаться с сервером.
err_timeout|Сервер не ответил вовремя.
err_unknown|Непредвиденная ошибка ({0}).
"""

LANGS['uk'] = """
extName|Stream Transcription
extDescription|Субтитри наживо для будь-якої вкладки: розпізнає й перекладає ваш власний сервер Whisper.
start|Увімкнути субтитри
stop|Вимкнути субтитри
status_idle|Готово
status_connecting|Підключення…
status_loading|Завантаження моделі…
status_listening|Слухаю…
status_live|Наживо
status_stalled|Звук зупинено
status_error|Помилка
status_noresponse|Немає відповіді
model|Модель
model_server_default|Як на сервері
model_default_tag|{0} · типова
manage_models|Керувати моделями
spoken_lang|Мова аудіо
auto_detect|Автоматично
detected|Визначено: {0}
subs_lang|Субтитри мовою
original_lang|Без перекладу
lines|Рядки
text_size|Розмір тексту
save_srt|Зберігати субтитри (.srt) під час зупинки
advanced|Додатково
use_vad|Пропускати тишу (виявлення мовлення)
settings|Налаштування
first_load_hint|Першого разу завантаження моделі може тривати до хвилини.
options_locked|Вимкніть субтитри, щоб змінити ці параметри.
server_setup_title|Підключіть свій сервер
server_setup_hint|Stream Transcription потрібен сервер WhisperLive на вашому комп’ютері або у вашій мережі.
server_address|Адреса сервера
server_placeholder|напр. localhost:9090 або 192.168.1.10:9090
connect|Підключити
server_ok_models|Підключено · моделей: {0}
server_ok_one_model|Підключено · 1 модель
server_plain|Підключено · стандартний WhisperLive (без керування моделями)
server_checking|Перевірка…
server_unreachable|Не вдається зв’язатися із сервером. Він увімкнений? Перевірте адресу й брандмауер.
server_timeout|Сервер не відповів вчасно.
server_bad_url|Ця адреса недійсна.
server_change|Змінити
server_help|Як налаштувати сервер?
server_help_1|Потрібен сервер WhisperLive (вільний і безкоштовний) на комп’ютері, краще з відеокартою NVIDIA. Невеликі моделі працюють і на самому процесорі.
server_help_2|Потім введіть тут його адресу: IP комп’ютера й порт, напр. 192.168.1.10:9090. Якщо він на цьому ж комп’ютері — localhost:9090.
server_help_3|Щоб завантажувати моделі й керувати ними з цієї сторінки, додайте на сервер доповнення Stream Transcription.
server_help_guide|Покроковий посібник
error_capture|Цю вкладку неможливо захопити (сторінки браузера, крамниці розширень і PDF недоступні).
error_no_media|На цій сторінці немає ні відео, ні звуку.
error_server_full|Сервер зайнятий. Орієнтовне очікування: {0} хв.
error_disconnected|Сервер закрив з’єднання.
error_model_load|⚠ На сервері бракує відеопам’яті (VRAM) для цієї моделі. Виберіть меншу модель або ввімкніть «Заощаджувати пам’ять (int8)» у розділі «Додатково».
warn_no_response|⚠ Субтитри перестали надходити, хоча звук є. Імовірно, модель не вміщується у відеопам’ять (VRAM) сервера: виберіть меншу модель або ввімкніть «Заощаджувати пам’ять (int8)» у розділі «Додатково».
warn_slow_load|⚠ Модель завантажується надто довго. Можливо, вона не вміщується у відеопам’ять (VRAM) сервера: виберіть меншу модель або ввімкніть «Заощаджувати пам’ять (int8)» у розділі «Додатково».
error_reload|Перезавантажте сторінку (F5) і почніть знову.
error_no_server|Спершу налаштуйте сервер.
settings_title|Stream Transcription · Налаштування
section_server|Сервер
section_models|Моделі
section_subtitles|Субтитри
section_interface|Інтерфейс
section_about|Про програму
installed_models|Встановлені на сервері
no_models|Моделей ще немає.
badge_default|Типова
badge_loaded|У пам’яті
badge_selected|Вибрана
use_model|Використати
delete_model|Видалити
confirm_delete|Видалити {0} із сервера? Звільниться {1}.
add_model|Додати модель
add_model_hint|Вставте назву або посилання на модель із Hugging Face. Підійде будь-яка модель Whisper: моделі faster-whisper (CTranslate2) використовуються як є, звичайні (transformers) конвертуються автоматично. Підійде й пряме посилання на .zip або .tar.gz із моделлю.
add_model_placeholder|напр. Systran/faster-whisper-large-v3
download|Завантажити
suggestions|Варіанти:
browse_hf|Переглянути моделі Whisper на Hugging Face
vram_hint|Більші моделі точніші, але потребують більше відеопам’яті: small ≈ 1 ГБ, medium ≈ 2 ГБ, large ≈ 4 ГБ.
keep_open|Не закривайте цю сторінку, доки завантаження не завершиться.
job_downloading|Завантаження… {0} із {1}
job_downloading_nosize|Завантаження… {0}
job_converting|Конвертація у формат faster-whisper…
job_extracting|Розпакування…
job_ready|Встановлено
job_error|Не вдалося: {0}
retry|Повторити
plain_server_hint|Це стандартний сервер WhisperLive: введіть розмір моделі (tiny, base, small, medium, large-v3, large-v3-turbo), і сервер завантажить її першого разу. Щоб завантажувати звідси будь-які моделі, встановіть на сервер доповнення Stream Transcription.
model_name|Назва моделі
save|Зберегти
saved|Збережено
reset_position|Скинути положення субтитрів
position_reset_done|Готово: вони повернуться вниз.
section_performance|Продуктивність
performance_hint|Якщо відеокарті сервера бракує пам’яті (субтитри не надходять або з’являється попередження про пам’ять), ці два параметри звільняють чимало. Працюють лише із сервером Stream Transcription.
precision|Точність моделі
precision_auto|Автоматично
precision_int8|Заощаджувати пам’ять (int8)
precision_hint|int8 займає приблизно половину відеопам’яті й на практиці пише той самий текст.
translator_device|Перекладач працює на
device_gpu|Відеокарті
device_cpu|Процесорі (CPU)
translator_device_hint|На процесорі звільняється відеопам’ять, але перекладені субтитри надходять трохи пізніше.
interface_lang|Мова інтерфейсу
lang_auto|Як у браузері
about_text|Вільне ПЗ (ліцензія MIT). Звук іде лише на сервер, який ви тут укажете; більше нікуди нічого не надсилається.
about_based|На основі WhisperLive від Collabora.
source_code|Вихідний код
subtitle_preview|Так виглядатимуть ваші субтитри.
err_invalid_source|Це не назва моделі Hugging Face і не посилання.
err_unsupported_url|Лише посилання на Hugging Face або прямі посилання на файли .zip / .tar.gz.
err_repo_not_found|Такої моделі на Hugging Face немає (перевірте назву).
err_gated_repo|Для цієї моделі треба прийняти умови на Hugging Face; серверу потрібен HF_TOKEN.
err_not_whisper|Це не модель Whisper.
err_no_weights|У цьому репозиторії немає ваг моделі.
err_network_error|Помилка мережі. Повторіть: продовжить із того місця, де зупинилося.
err_download_failed|Завантаження не вдалося.
err_convert_failed|Не вдалося конвертувати модель.
err_bad_archive|Архів пошкоджений або небезпечний.
err_already_downloading|Уже завантажується.
err_already_installed|Уже встановлена.
err_management_disabled|Керування моделями на цьому сервері вимкнено.
err_is_default|Це типова модель сервера; видалити її звідси неможливо.
err_in_use|Її використовує поточна транскрипція.
err_not_found|Цієї моделі на сервері вже немає.
err_server_error|Помилка сервера.
err_unreachable|Не вдається зв’язатися із сервером.
err_timeout|Сервер не відповів вчасно.
err_unknown|Неочікувана помилка ({0}).
"""

LANGS['zh_CN'] = """
extName|Stream Transcription
extDescription|为任意标签页提供实时字幕，由你自己的 Whisper 服务器转写和翻译。
start|开启字幕
stop|关闭字幕
status_idle|就绪
status_connecting|正在连接…
status_loading|正在加载模型…
status_listening|正在收听…
status_live|直播中
status_stalled|音频已停止
status_error|错误
status_noresponse|无响应
model|模型
model_server_default|服务器默认
model_default_tag|{0} · 默认
manage_models|管理模型
spoken_lang|音频语言
auto_detect|自动检测
detected|检测到：{0}
subs_lang|字幕语言
original_lang|不翻译
lines|行数
text_size|文字大小
save_srt|停止时保存字幕 (.srt)
advanced|高级
use_vad|跳过静音（语音检测）
settings|设置
first_load_hint|首次加载模型可能需要一分钟左右。
options_locked|关闭字幕后才能更改这些选项。
server_setup_title|连接你的服务器
server_setup_hint|Stream Transcription 需要在你的电脑或网络中运行 WhisperLive 服务器。
server_address|服务器地址
server_placeholder|例如 localhost:9090 或 192.168.1.10:9090
connect|连接
server_ok_models|已连接 · {0} 个模型
server_ok_one_model|已连接 · 1 个模型
server_plain|已连接 · 标准 WhisperLive（无模型管理）
server_checking|正在检查…
server_unreachable|无法连接服务器。它在运行吗？请检查地址和防火墙。
server_timeout|服务器未及时响应。
server_bad_url|该地址无效。
server_change|更改
server_help|如何搭建服务器？
server_help_1|你需要在一台电脑上运行 WhisperLive 服务器（免费开源），最好有 NVIDIA 显卡。小模型只用处理器也能运行。
server_help_2|然后在这里输入它的地址：电脑的 IP 和端口，例如 192.168.1.10:9090。如果就在这台电脑上，填 localhost:9090。
server_help_3|要在此页面下载和管理模型，请给服务器加装 Stream Transcription 插件。
server_help_guide|分步指南
error_capture|无法捕获此标签页（浏览器页面、扩展商店和 PDF 不允许）。
error_no_media|此页面没有视频或音频。
error_server_full|服务器繁忙。预计等待：{0} 分钟。
error_disconnected|服务器关闭了连接。
error_model_load|⚠ 服务器的显存 (VRAM) 不足以运行此模型。请选择更小的模型，或在“高级”中开启“节省内存 (int8)”。
warn_no_response|⚠ 虽然有声音，但字幕不再出现。可能是模型放不进服务器的显存 (VRAM)：请选择更小的模型，或在“高级”中开启“节省内存 (int8)”。
warn_slow_load|⚠ 模型加载时间过长。可能放不进服务器的显存 (VRAM)：请选择更小的模型，或在“高级”中开启“节省内存 (int8)”。
error_reload|请刷新页面 (F5) 后重新开始。
error_no_server|请先设置服务器。
settings_title|Stream Transcription · 设置
section_server|服务器
section_models|模型
section_subtitles|字幕
section_interface|界面
section_about|关于
installed_models|服务器上已安装
no_models|还没有安装模型。
badge_default|默认
badge_loaded|已在内存中
badge_selected|已选择
use_model|使用
delete_model|删除
confirm_delete|从服务器删除 {0}？可释放 {1}。
add_model|添加模型
add_model_hint|粘贴 Hugging Face 上模型的名称或链接。任何 Whisper 模型都可以：faster-whisper (CTranslate2) 模型直接使用，普通 (transformers) 模型会自动转换。指向包含模型的 .zip 或 .tar.gz 的直链也可以。
add_model_placeholder|例如 Systran/faster-whisper-large-v3
download|下载
suggestions|推荐：
browse_hf|在 Hugging Face 浏览 Whisper 模型
vram_hint|模型越大越准确，但需要更多显存：small ≈ 1 GB，medium ≈ 2 GB，large ≈ 4 GB。
keep_open|下载完成前请保持此页面打开。
job_downloading|正在下载… {0} / {1}
job_downloading_nosize|正在下载… {0}
job_converting|正在转换为 faster-whisper 格式…
job_extracting|正在解压…
job_ready|已安装
job_error|失败：{0}
retry|重试
plain_server_hint|这是标准的 WhisperLive 服务器：输入模型大小（tiny、base、small、medium、large-v3、large-v3-turbo），服务器会在首次使用时下载。要从这里下载任意模型，请在服务器上安装 Stream Transcription 插件。
model_name|模型名称
save|保存
saved|已保存
reset_position|重置字幕位置
position_reset_done|完成：字幕会回到底部。
section_performance|性能
performance_hint|如果服务器显卡内存不足（字幕不出现或出现内存警告），这两个选项可以释放大量内存。仅适用于 Stream Transcription 服务器。
precision|模型精度
precision_auto|自动
precision_int8|节省内存 (int8)
precision_hint|int8 大约只用一半显存，实际写出的文字基本相同。
translator_device|翻译器运行在
device_gpu|显卡
device_cpu|处理器 (CPU)
translator_device_hint|放在处理器上可以释放显存，但翻译后的字幕会稍晚一些。
interface_lang|界面语言
lang_auto|跟随浏览器
about_text|自由软件（MIT 许可证）。音频只会发送到你在这里设置的服务器，不会发往其他任何地方。
about_based|基于 Collabora 的 WhisperLive。
source_code|源代码
subtitle_preview|你的字幕会是这个样子。
err_invalid_source|这不是 Hugging Face 的模型名称，也不是链接。
err_unsupported_url|只支持 Hugging Face 链接或指向 .zip / .tar.gz 文件的直链。
err_repo_not_found|Hugging Face 上没有这个模型（请检查名称）。
err_gated_repo|该模型要求在 Hugging Face 上接受条款；服务器需要 HF_TOKEN。
err_not_whisper|这不是 Whisper 模型。
err_no_weights|该仓库没有模型权重。
err_network_error|网络错误。请重试：会从中断处继续。
err_download_failed|下载失败。
err_convert_failed|无法转换模型。
err_bad_archive|压缩包已损坏或不安全。
err_already_downloading|已在下载中。
err_already_installed|已经安装。
err_management_disabled|此服务器已关闭模型管理。
err_is_default|这是服务器的默认模型，不能在这里删除。
err_in_use|正在进行的转写正在使用它。
err_not_found|服务器上已没有这个模型。
err_server_error|服务器错误。
err_unreachable|无法连接服务器。
err_timeout|服务器未及时响应。
err_unknown|意外错误（{0}）。
"""

LANGS['ja'] = """
extName|Stream Transcription
extDescription|どのタブにもリアルタイム字幕。自分の Whisper サーバーが文字起こしと翻訳をします。
start|字幕をオン
stop|字幕をオフ
status_idle|準備完了
status_connecting|接続中…
status_loading|モデルを読み込み中…
status_listening|聞き取り中…
status_live|ライブ
status_stalled|音声が止まりました
status_error|エラー
status_noresponse|応答なし
model|モデル
model_server_default|サーバーの既定
model_default_tag|{0} · 既定
manage_models|モデルを管理
spoken_lang|音声の言語
auto_detect|自動検出
detected|検出：{0}
subs_lang|字幕の言語
original_lang|翻訳しない
lines|行数
text_size|文字サイズ
save_srt|停止時に字幕 (.srt) を保存
advanced|詳細設定
use_vad|無音をスキップ（音声検出）
settings|設定
first_load_hint|モデルの初回読み込みには最大 1 分ほどかかることがあります。
options_locked|これらの設定を変えるには字幕をオフにしてください。
server_setup_title|サーバーに接続
server_setup_hint|Stream Transcription には、パソコンかネットワーク上で動く WhisperLive サーバーが必要です。
server_address|サーバーのアドレス
server_placeholder|例：localhost:9090 または 192.168.1.10:9090
connect|接続
server_ok_models|接続済み · モデル {0} 個
server_ok_one_model|接続済み · モデル 1 個
server_plain|接続済み · 標準の WhisperLive（モデル管理なし）
server_checking|確認中…
server_unreachable|サーバーに接続できません。起動していますか？アドレスとファイアウォールを確認してください。
server_timeout|サーバーが時間内に応答しませんでした。
server_bad_url|このアドレスは無効です。
server_change|変更
server_help|サーバーの用意のしかた
server_help_1|パソコンで WhisperLive サーバー（無料のオープンソース）を動かします。NVIDIA のグラフィックボードがあると理想的です。小さなモデルは CPU だけでも動きます。
server_help_2|次にここにアドレスを入力します：パソコンの IP とポート、例 192.168.1.10:9090。同じパソコンで動かすなら localhost:9090。
server_help_3|このページからモデルをダウンロード・管理するには、サーバーに Stream Transcription のアドオンを追加してください。
server_help_guide|手順ガイド
error_capture|このタブはキャプチャできません（ブラウザーのページ、拡張機能ストア、PDF は対象外です）。
error_no_media|このページには動画も音声もありません。
error_server_full|サーバーが混雑しています。待ち時間の目安：{0} 分。
error_disconnected|サーバーが接続を閉じました。
error_model_load|⚠ このモデルにはサーバーのビデオメモリ (VRAM) が足りません。小さいモデルを選ぶか、詳細設定で「メモリを節約 (int8)」をオンにしてください。
warn_no_response|⚠ 音が出ているのに字幕が届かなくなりました。モデルがサーバーのビデオメモリ (VRAM) に収まっていないようです。小さいモデルを選ぶか、詳細設定で「メモリを節約 (int8)」をオンにしてください。
warn_slow_load|⚠ モデルの読み込みに時間がかかりすぎています。サーバーのビデオメモリ (VRAM) に収まらないのかもしれません。小さいモデルを選ぶか、詳細設定で「メモリを節約 (int8)」をオンにしてください。
error_reload|ページを再読み込み (F5) して、もう一度始めてください。
error_no_server|先にサーバーを設定してください。
settings_title|Stream Transcription · 設定
section_server|サーバー
section_models|モデル
section_subtitles|字幕
section_interface|インターフェース
section_about|このアプリについて
installed_models|サーバーにインストール済み
no_models|まだモデルがありません。
badge_default|既定
badge_loaded|メモリ上
badge_selected|選択中
use_model|使う
delete_model|削除
confirm_delete|{0} をサーバーから削除しますか？ {1} が空きます。
add_model|モデルを追加
add_model_hint|Hugging Face のモデル名かリンクを貼り付けてください。Whisper モデルなら何でも使えます。faster-whisper (CTranslate2) のモデルはそのまま、通常の (transformers) モデルは自動で変換されます。モデル入りの .zip や .tar.gz への直接リンクも使えます。
add_model_placeholder|例：Systran/faster-whisper-large-v3
download|ダウンロード
suggestions|おすすめ：
browse_hf|Hugging Face で Whisper モデルを見る
vram_hint|大きいモデルほど正確ですが、ビデオメモリを多く使います：small ≈ 1 GB、medium ≈ 2 GB、large ≈ 4 GB。
keep_open|ダウンロードが終わるまでこのページを開いたままにしてください。
job_downloading|ダウンロード中… {0} / {1}
job_downloading_nosize|ダウンロード中… {0}
job_converting|faster-whisper 形式に変換中…
job_extracting|展開中…
job_ready|インストール済み
job_error|失敗：{0}
retry|再試行
plain_server_hint|標準の WhisperLive サーバーです。モデルのサイズ（tiny、base、small、medium、large-v3、large-v3-turbo）を入力すると、初回にサーバーがダウンロードします。ここから任意のモデルをダウンロードするには、サーバーに Stream Transcription のアドオンを入れてください。
model_name|モデル名
save|保存
saved|保存しました
reset_position|字幕の位置をリセット
position_reset_done|完了：下に戻ります。
section_performance|パフォーマンス
performance_hint|サーバーのグラフィックボードのメモリが足りないとき（字幕が届かない、メモリの警告が出る）、この 2 つの設定で大きく空けられます。Stream Transcription のサーバーでのみ有効です。
precision|モデルの精度
precision_auto|自動
precision_int8|メモリを節約 (int8)
precision_hint|int8 はビデオメモリを約半分しか使わず、実際にはほぼ同じ文字を書き出します。
translator_device|翻訳を実行する場所
device_gpu|GPU
device_cpu|CPU
translator_device_hint|CPU で動かすとビデオメモリが空きますが、翻訳字幕は少し遅れて届きます。
interface_lang|表示言語
lang_auto|ブラウザーに合わせる
about_text|フリーソフトウェア（MIT ライセンス）。音声はここで設定したサーバーにだけ送られ、ほかには一切送られません。
about_based|Collabora の WhisperLive をもとにしています。
source_code|ソースコード
subtitle_preview|字幕はこのように表示されます。
err_invalid_source|Hugging Face のモデル名でもリンクでもありません。
err_unsupported_url|Hugging Face のリンクか、.zip / .tar.gz ファイルへの直接リンクのみです。
err_repo_not_found|そのモデルは Hugging Face にありません（名前を確認してください）。
err_gated_repo|そのモデルは Hugging Face で利用条件への同意が必要です。サーバーに HF_TOKEN が必要です。
err_not_whisper|Whisper モデルではありません。
err_no_weights|そのリポジトリにはモデルの重みがありません。
err_network_error|ネットワークエラー。再試行すると、止まったところから続きます。
err_download_failed|ダウンロードに失敗しました。
err_convert_failed|モデルを変換できませんでした。
err_bad_archive|アーカイブが壊れているか、安全ではありません。
err_already_downloading|すでにダウンロード中です。
err_already_installed|すでにインストールされています。
err_management_disabled|このサーバーではモデル管理が無効です。
err_is_default|サーバーの既定のモデルなので、ここからは削除できません。
err_in_use|実行中の文字起こしが使用しています。
err_not_found|そのモデルはもうサーバーにありません。
err_server_error|サーバーエラー。
err_unreachable|サーバーに接続できません。
err_timeout|サーバーが時間内に応答しませんでした。
err_unknown|予期しないエラー（{0}）。
"""

LANGS['ko'] = """
extName|Stream Transcription
extDescription|어떤 탭에서든 실시간 자막. 내 Whisper 서버가 받아쓰고 번역합니다.
start|자막 켜기
stop|자막 끄기
status_idle|준비됨
status_connecting|연결 중…
status_loading|모델 불러오는 중…
status_listening|듣는 중…
status_live|실시간
status_stalled|오디오 멈춤
status_error|오류
status_noresponse|응답 없음
model|모델
model_server_default|서버 기본값
model_default_tag|{0} · 기본
manage_models|모델 관리
spoken_lang|오디오 언어
auto_detect|자동 감지
detected|감지됨: {0}
subs_lang|자막 언어
original_lang|번역 안 함
lines|줄 수
text_size|글자 크기
save_srt|끌 때 자막(.srt) 저장
advanced|고급
use_vad|무음 건너뛰기(음성 감지)
settings|설정
first_load_hint|모델을 처음 불러올 때는 최대 1분 정도 걸릴 수 있습니다.
options_locked|이 설정을 바꾸려면 자막을 끄세요.
server_setup_title|서버 연결
server_setup_hint|Stream Transcription을 쓰려면 컴퓨터나 네트워크에서 WhisperLive 서버가 실행 중이어야 합니다.
server_address|서버 주소
server_placeholder|예: localhost:9090 또는 192.168.1.10:9090
connect|연결
server_ok_models|연결됨 · 모델 {0}개
server_ok_one_model|연결됨 · 모델 1개
server_plain|연결됨 · 표준 WhisperLive(모델 관리 없음)
server_checking|확인 중…
server_unreachable|서버에 연결할 수 없습니다. 켜져 있나요? 주소와 방화벽을 확인하세요.
server_timeout|서버가 제때 응답하지 않았습니다.
server_bad_url|올바른 주소가 아닙니다.
server_change|변경
server_help|서버는 어떻게 준비하나요?
server_help_1|컴퓨터에서 WhisperLive 서버(무료 오픈 소스)를 실행해야 합니다. NVIDIA 그래픽 카드가 있으면 가장 좋습니다. 작은 모델은 프로세서만으로도 돌아갑니다.
server_help_2|그런 다음 여기에 주소를 입력하세요: 컴퓨터 IP와 포트, 예 192.168.1.10:9090. 같은 컴퓨터라면 localhost:9090.
server_help_3|이 페이지에서 모델을 내려받고 관리하려면 서버에 Stream Transcription 애드온을 추가하세요.
server_help_guide|단계별 안내
error_capture|이 탭은 캡처할 수 없습니다(브라우저 페이지, 확장 프로그램 스토어, PDF는 제외).
error_no_media|이 페이지에는 동영상이나 오디오가 없습니다.
error_server_full|서버가 바쁩니다. 예상 대기: {0}분.
error_disconnected|서버가 연결을 닫았습니다.
error_model_load|⚠ 서버의 그래픽 메모리(VRAM)가 이 모델에 부족합니다. 더 작은 모델을 고르거나 고급에서 ‘메모리 절약(int8)’을 켜세요.
warn_no_response|⚠ 소리가 나는데도 자막이 오지 않습니다. 모델이 서버의 그래픽 메모리(VRAM)에 들어가지 않는 것 같습니다. 더 작은 모델을 고르거나 고급에서 ‘메모리 절약(int8)’을 켜세요.
warn_slow_load|⚠ 모델을 불러오는 데 너무 오래 걸립니다. 서버의 그래픽 메모리(VRAM)에 들어가지 않을 수 있습니다. 더 작은 모델을 고르거나 고급에서 ‘메모리 절약(int8)’을 켜세요.
error_reload|페이지를 새로 고침(F5)하고 다시 시작하세요.
error_no_server|먼저 서버를 설정하세요.
settings_title|Stream Transcription · 설정
section_server|서버
section_models|모델
section_subtitles|자막
section_interface|인터페이스
section_about|정보
installed_models|서버에 설치됨
no_models|아직 설치된 모델이 없습니다.
badge_default|기본
badge_loaded|메모리에 있음
badge_selected|선택됨
use_model|사용
delete_model|삭제
confirm_delete|서버에서 {0}을(를) 삭제할까요? {1}이(가) 확보됩니다.
add_model|모델 추가
add_model_hint|Hugging Face 모델의 이름이나 링크를 붙여 넣으세요. 어떤 Whisper 모델이든 됩니다. faster-whisper(CTranslate2) 모델은 그대로 쓰고, 일반(transformers) 모델은 자동으로 변환합니다. 모델이 든 .zip이나 .tar.gz 직접 링크도 됩니다.
add_model_placeholder|예: Systran/faster-whisper-large-v3
download|내려받기
suggestions|추천:
browse_hf|Hugging Face에서 Whisper 모델 보기
vram_hint|큰 모델일수록 정확하지만 그래픽 메모리를 더 씁니다: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB.
keep_open|내려받기가 끝날 때까지 이 페이지를 열어 두세요.
job_downloading|내려받는 중… {0} / {1}
job_downloading_nosize|내려받는 중… {0}
job_converting|faster-whisper 형식으로 변환 중…
job_extracting|압축 푸는 중…
job_ready|설치됨
job_error|실패: {0}
retry|다시 시도
plain_server_hint|표준 WhisperLive 서버입니다. 모델 크기(tiny, base, small, medium, large-v3, large-v3-turbo)를 입력하면 서버가 처음에 내려받습니다. 여기서 아무 모델이나 내려받으려면 서버에 Stream Transcription 애드온을 설치하세요.
model_name|모델 이름
save|저장
saved|저장됨
reset_position|자막 위치 초기화
position_reset_done|완료: 다시 아래로 갑니다.
section_performance|성능
performance_hint|서버 그래픽 카드의 메모리가 모자라면(자막이 오지 않거나 메모리 경고가 뜨면) 이 두 옵션으로 꽤 많이 확보할 수 있습니다. Stream Transcription 서버에서만 작동합니다.
precision|모델 정밀도
precision_auto|자동
precision_int8|메모리 절약(int8)
precision_hint|int8은 그래픽 메모리를 절반쯤만 쓰며, 실제로는 같은 글을 씁니다.
translator_device|번역기 실행 위치
device_gpu|그래픽 카드
device_cpu|프로세서(CPU)
translator_device_hint|프로세서에서 돌리면 그래픽 메모리가 확보되지만 번역 자막이 조금 늦게 옵니다.
interface_lang|인터페이스 언어
lang_auto|브라우저와 같게
about_text|자유 소프트웨어(MIT 라이선스). 오디오는 여기서 설정한 서버로만 가며, 다른 곳으로는 아무것도 보내지 않습니다.
about_based|Collabora의 WhisperLive를 바탕으로 합니다.
source_code|소스 코드
subtitle_preview|자막은 이렇게 보입니다.
err_invalid_source|Hugging Face 모델 이름도 링크도 아닙니다.
err_unsupported_url|Hugging Face 링크나 .zip / .tar.gz 파일 직접 링크만 됩니다.
err_repo_not_found|그런 모델이 Hugging Face에 없습니다(이름을 확인하세요).
err_gated_repo|이 모델은 Hugging Face에서 이용 조건에 동의해야 합니다. 서버에 HF_TOKEN이 필요합니다.
err_not_whisper|Whisper 모델이 아닙니다.
err_no_weights|이 저장소에는 모델 가중치가 없습니다.
err_network_error|네트워크 오류입니다. 다시 시도하면 멈춘 곳부터 이어집니다.
err_download_failed|내려받기에 실패했습니다.
err_convert_failed|모델을 변환하지 못했습니다.
err_bad_archive|압축 파일이 손상되었거나 안전하지 않습니다.
err_already_downloading|이미 내려받는 중입니다.
err_already_installed|이미 설치되어 있습니다.
err_management_disabled|이 서버에서는 모델 관리가 꺼져 있습니다.
err_is_default|서버의 기본 모델이라 여기서 삭제할 수 없습니다.
err_in_use|진행 중인 받아쓰기가 사용하고 있습니다.
err_not_found|그 모델은 더 이상 서버에 없습니다.
err_server_error|서버 오류.
err_unreachable|서버에 연결할 수 없습니다.
err_timeout|서버가 제때 응답하지 않았습니다.
err_unknown|예상치 못한 오류({0}).
"""

LANGS['th'] = """
extName|Stream Transcription
extDescription|คำบรรยายสดสำหรับทุกแท็บ ถอดความและแปลโดยเซิร์ฟเวอร์ Whisper ของคุณเอง
start|เปิดคำบรรยาย
stop|ปิดคำบรรยาย
status_idle|พร้อม
status_connecting|กำลังเชื่อมต่อ…
status_loading|กำลังโหลดโมเดล…
status_listening|กำลังฟัง…
status_live|สด
status_stalled|เสียงหยุดแล้ว
status_error|ข้อผิดพลาด
status_noresponse|ไม่มีการตอบกลับ
model|โมเดล
model_server_default|ค่าเริ่มต้นของเซิร์ฟเวอร์
model_default_tag|{0} · ค่าเริ่มต้น
manage_models|จัดการโมเดล
spoken_lang|ภาษาของเสียง
auto_detect|ตรวจหาอัตโนมัติ
detected|ตรวจพบ: {0}
subs_lang|คำบรรยายเป็นภาษา
original_lang|ไม่แปล
lines|จำนวนบรรทัด
text_size|ขนาดตัวอักษร
save_srt|บันทึกคำบรรยาย (.srt) เมื่อหยุด
advanced|ขั้นสูง
use_vad|ข้ามช่วงเงียบ (ตรวจจับเสียงพูด)
settings|การตั้งค่า
first_load_hint|การโหลดโมเดลครั้งแรกอาจใช้เวลาถึงหนึ่งนาที
options_locked|ปิดคำบรรยายก่อนจึงจะเปลี่ยนตัวเลือกเหล่านี้ได้
server_setup_title|เชื่อมต่อเซิร์ฟเวอร์ของคุณ
server_setup_hint|Stream Transcription ต้องใช้เซิร์ฟเวอร์ WhisperLive ที่ทำงานบนคอมพิวเตอร์หรือในเครือข่ายของคุณ
server_address|ที่อยู่เซิร์ฟเวอร์
server_placeholder|เช่น localhost:9090 หรือ 192.168.1.10:9090
connect|เชื่อมต่อ
server_ok_models|เชื่อมต่อแล้ว · {0} โมเดล
server_ok_one_model|เชื่อมต่อแล้ว · 1 โมเดล
server_plain|เชื่อมต่อแล้ว · WhisperLive มาตรฐาน (ไม่มีการจัดการโมเดล)
server_checking|กำลังตรวจสอบ…
server_unreachable|ติดต่อเซิร์ฟเวอร์ไม่ได้ เปิดอยู่หรือไม่ ตรวจสอบที่อยู่และไฟร์วอลล์
server_timeout|เซิร์ฟเวอร์ไม่ตอบกลับทันเวลา
server_bad_url|ที่อยู่นี้ไม่ถูกต้อง
server_change|เปลี่ยน
server_help|จะตั้งเซิร์ฟเวอร์อย่างไร
server_help_1|คุณต้องมีเซิร์ฟเวอร์ WhisperLive (ฟรีและโอเพนซอร์ส) บนคอมพิวเตอร์ ถ้ามีการ์ดจอ NVIDIA จะดีที่สุด โมเดลเล็กใช้แค่ซีพียูก็ได้
server_help_2|จากนั้นพิมพ์ที่อยู่ของมันที่นี่: IP ของคอมพิวเตอร์และพอร์ต เช่น 192.168.1.10:9090 ถ้าอยู่บนคอมพิวเตอร์เครื่องนี้ ให้ใช้ localhost:9090
server_help_3|หากต้องการดาวน์โหลดและจัดการโมเดลจากหน้านี้ ให้ติดตั้งส่วนเสริม Stream Transcription บนเซิร์ฟเวอร์
server_help_guide|คู่มือทีละขั้นตอน
error_capture|จับภาพแท็บนี้ไม่ได้ (หน้าของเบราว์เซอร์ ร้านส่วนขยาย และ PDF ใช้ไม่ได้)
error_no_media|หน้านี้ไม่มีวิดีโอหรือเสียง
error_server_full|เซิร์ฟเวอร์ไม่ว่าง เวลารอโดยประมาณ: {0} นาที
error_disconnected|เซิร์ฟเวอร์ปิดการเชื่อมต่อแล้ว
error_model_load|⚠ หน่วยความจำกราฟิก (VRAM) ของเซิร์ฟเวอร์ไม่พอสำหรับโมเดลนี้ เลือกโมเดลที่เล็กลง หรือเปิด “ประหยัดหน่วยความจำ (int8)” ในขั้นสูง
warn_no_response|⚠ คำบรรยายหยุดมาทั้งที่มีเสียง โมเดลอาจใส่ไม่พอในหน่วยความจำกราฟิก (VRAM) ของเซิร์ฟเวอร์ เลือกโมเดลที่เล็กลง หรือเปิด “ประหยัดหน่วยความจำ (int8)” ในขั้นสูง
warn_slow_load|⚠ โมเดลโหลดนานเกินไป อาจใส่ไม่พอในหน่วยความจำกราฟิก (VRAM) ของเซิร์ฟเวอร์ เลือกโมเดลที่เล็กลง หรือเปิด “ประหยัดหน่วยความจำ (int8)” ในขั้นสูง
error_reload|โหลดหน้าใหม่ (F5) แล้วเริ่มอีกครั้ง
error_no_server|ตั้งค่าเซิร์ฟเวอร์ก่อน
settings_title|Stream Transcription · การตั้งค่า
section_server|เซิร์ฟเวอร์
section_models|โมเดล
section_subtitles|คำบรรยาย
section_interface|หน้าตาโปรแกรม
section_about|เกี่ยวกับ
installed_models|ติดตั้งบนเซิร์ฟเวอร์แล้ว
no_models|ยังไม่มีโมเดลที่ติดตั้ง
badge_default|ค่าเริ่มต้น
badge_loaded|อยู่ในหน่วยความจำ
badge_selected|เลือกแล้ว
use_model|ใช้
delete_model|ลบ
confirm_delete|ลบ {0} ออกจากเซิร์ฟเวอร์ไหม จะได้พื้นที่คืน {1}
add_model|เพิ่มโมเดล
add_model_hint|วางชื่อหรือลิงก์ของโมเดลจาก Hugging Face ใช้โมเดล Whisper ใดก็ได้ โมเดล faster-whisper (CTranslate2) ใช้ได้ทันที ส่วนโมเดลทั่วไป (transformers) จะถูกแปลงให้เอง ลิงก์ตรงไปยัง .zip หรือ .tar.gz ที่มีโมเดลก็ใช้ได้
add_model_placeholder|เช่น Systran/faster-whisper-large-v3
download|ดาวน์โหลด
suggestions|แนะนำ:
browse_hf|ดูโมเดล Whisper บน Hugging Face
vram_hint|โมเดลใหญ่แม่นยำกว่าแต่ใช้หน่วยความจำการ์ดจอมากกว่า: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB
keep_open|เปิดหน้านี้ค้างไว้จนกว่าจะดาวน์โหลดเสร็จ
job_downloading|กำลังดาวน์โหลด… {0} จาก {1}
job_downloading_nosize|กำลังดาวน์โหลด… {0}
job_converting|กำลังแปลงเป็นรูปแบบ faster-whisper…
job_extracting|กำลังแตกไฟล์…
job_ready|ติดตั้งแล้ว
job_error|ล้มเหลว: {0}
retry|ลองอีกครั้ง
plain_server_hint|นี่คือเซิร์ฟเวอร์ WhisperLive มาตรฐาน: พิมพ์ขนาดโมเดล (tiny, base, small, medium, large-v3, large-v3-turbo) แล้วเซิร์ฟเวอร์จะดาวน์โหลดในครั้งแรก หากต้องการดาวน์โหลดโมเดลใดก็ได้จากที่นี่ ให้ติดตั้งส่วนเสริม Stream Transcription บนเซิร์ฟเวอร์
model_name|ชื่อโมเดล
save|บันทึก
saved|บันทึกแล้ว
reset_position|รีเซ็ตตำแหน่งคำบรรยาย
position_reset_done|เรียบร้อย: จะกลับไปอยู่ด้านล่าง
section_performance|ประสิทธิภาพ
performance_hint|หากการ์ดจอของเซิร์ฟเวอร์หน่วยความจำไม่พอ (คำบรรยายไม่มาหรือมีคำเตือนเรื่องหน่วยความจำ) สองตัวเลือกนี้ช่วยคืนพื้นที่ได้มาก ใช้ได้กับเซิร์ฟเวอร์ Stream Transcription เท่านั้น
precision|ความแม่นยำของโมเดล
precision_auto|อัตโนมัติ
precision_int8|ประหยัดหน่วยความจำ (int8)
precision_hint|int8 ใช้หน่วยความจำกราฟิกราวครึ่งหนึ่ง และในทางปฏิบัติเขียนข้อความเหมือนเดิม
translator_device|ตัวแปลทำงานบน
device_gpu|การ์ดจอ
device_cpu|ซีพียู (CPU)
translator_device_hint|บนซีพียูจะคืนหน่วยความจำกราฟิก แต่คำบรรยายที่แปลแล้วจะมาช้าขึ้นเล็กน้อย
interface_lang|ภาษาของหน้าตาโปรแกรม
lang_auto|ตามเบราว์เซอร์
about_text|ซอฟต์แวร์เสรี (สัญญาอนุญาต MIT) เสียงจะส่งไปยังเซิร์ฟเวอร์ที่คุณตั้งไว้ที่นี่เท่านั้น ไม่มีการส่งไปที่อื่น
about_based|พัฒนาจาก WhisperLive ของ Collabora
source_code|ซอร์สโค้ด
subtitle_preview|คำบรรยายของคุณจะมีหน้าตาแบบนี้
err_invalid_source|นี่ไม่ใช่ชื่อโมเดลของ Hugging Face และไม่ใช่ลิงก์
err_unsupported_url|ใช้ได้เฉพาะลิงก์ Hugging Face หรือลิงก์ตรงไปยังไฟล์ .zip / .tar.gz
err_repo_not_found|ไม่มีโมเดลนี้บน Hugging Face (ตรวจชื่ออีกครั้ง)
err_gated_repo|โมเดลนี้ต้องยอมรับเงื่อนไขบน Hugging Face เซิร์ฟเวอร์ต้องมี HF_TOKEN
err_not_whisper|นี่ไม่ใช่โมเดล Whisper
err_no_weights|ที่เก็บนี้ไม่มีค่าน้ำหนักของโมเดล
err_network_error|เครือข่ายผิดพลาด ลองอีกครั้ง: จะทำต่อจากจุดที่หยุด
err_download_failed|ดาวน์โหลดไม่สำเร็จ
err_convert_failed|แปลงโมเดลไม่ได้
err_bad_archive|ไฟล์บีบอัดเสียหายหรือไม่ปลอดภัย
err_already_downloading|กำลังดาวน์โหลดอยู่แล้ว
err_already_installed|ติดตั้งแล้ว
err_management_disabled|เซิร์ฟเวอร์นี้ปิดการจัดการโมเดลไว้
err_is_default|นี่คือโมเดลค่าเริ่มต้นของเซิร์ฟเวอร์ ลบจากที่นี่ไม่ได้
err_in_use|มีการถอดความที่กำลังทำงานใช้อยู่
err_not_found|โมเดลนี้ไม่อยู่บนเซิร์ฟเวอร์แล้ว
err_server_error|เซิร์ฟเวอร์ผิดพลาด
err_unreachable|ติดต่อเซิร์ฟเวอร์ไม่ได้
err_timeout|เซิร์ฟเวอร์ไม่ตอบกลับทันเวลา
err_unknown|ข้อผิดพลาดที่ไม่คาดคิด ({0})
"""

LANGS['hi'] = """
extName|Stream Transcription
extDescription|किसी भी टैब के लिए लाइव सबटाइटल, जिन्हें आपका अपना Whisper सर्वर लिखता और अनुवाद करता है।
start|सबटाइटल चालू करें
stop|सबटाइटल बंद करें
status_idle|तैयार
status_connecting|कनेक्ट हो रहा है…
status_loading|मॉडल लोड हो रहा है…
status_listening|सुन रहा है…
status_live|लाइव
status_stalled|ऑडियो रुक गया
status_error|त्रुटि
status_noresponse|कोई जवाब नहीं
model|मॉडल
model_server_default|सर्वर का डिफ़ॉल्ट
model_default_tag|{0} · डिफ़ॉल्ट
manage_models|मॉडल प्रबंधित करें
spoken_lang|ऑडियो की भाषा
auto_detect|अपने-आप पहचानें
detected|पहचानी गई: {0}
subs_lang|सबटाइटल की भाषा
original_lang|अनुवाद नहीं
lines|पंक्तियाँ
text_size|टेक्स्ट का आकार
save_srt|बंद करते समय सबटाइटल (.srt) सेव करें
advanced|उन्नत
use_vad|ख़ामोशी छोड़ें (आवाज़ की पहचान)
settings|सेटिंग
first_load_hint|पहली बार मॉडल लोड होने में एक मिनट तक लग सकता है।
options_locked|ये विकल्प बदलने के लिए सबटाइटल बंद करें।
server_setup_title|अपना सर्वर कनेक्ट करें
server_setup_hint|Stream Transcription को आपके कंप्यूटर या नेटवर्क पर चलता WhisperLive सर्वर चाहिए।
server_address|सर्वर का पता
server_placeholder|जैसे localhost:9090 या 192.168.1.10:9090
connect|कनेक्ट करें
server_ok_models|कनेक्ट हो गया · {0} मॉडल
server_ok_one_model|कनेक्ट हो गया · 1 मॉडल
server_plain|कनेक्ट हो गया · सामान्य WhisperLive (मॉडल प्रबंधन नहीं)
server_checking|जाँच हो रही है…
server_unreachable|सर्वर से कनेक्ट नहीं हो पा रहा। क्या वह चालू है? पता और फ़ायरवॉल जाँचें।
server_timeout|सर्वर ने समय पर जवाब नहीं दिया।
server_bad_url|यह पता सही नहीं है।
server_change|बदलें
server_help|सर्वर कैसे सेट करें?
server_help_1|आपको किसी कंप्यूटर पर WhisperLive सर्वर (मुफ़्त और ओपन सोर्स) चलाना होगा, अच्छा हो कि NVIDIA ग्राफ़िक्स कार्ड हो। छोटे मॉडल सिर्फ़ प्रोसेसर पर भी चलते हैं।
server_help_2|फिर उसका पता यहाँ लिखें: कंप्यूटर का IP और पोर्ट, जैसे 192.168.1.10:9090। अगर इसी कंप्यूटर पर है, तो localhost:9090।
server_help_3|इस पेज से मॉडल डाउनलोड और प्रबंधित करने के लिए सर्वर में Stream Transcription ऐड-ऑन जोड़ें।
server_help_guide|क़दम-दर-क़दम गाइड
error_capture|यह टैब कैप्चर नहीं हो सकता (ब्राउज़र के पेज, एक्सटेंशन स्टोर और PDF की अनुमति नहीं)।
error_no_media|इस पेज पर न वीडियो है न ऑडियो।
error_server_full|सर्वर व्यस्त है। अनुमानित इंतज़ार: {0} मिनट।
error_disconnected|सर्वर ने कनेक्शन बंद कर दिया।
error_model_load|⚠ इस मॉडल के लिए सर्वर पर ग्राफ़िक्स मेमोरी (VRAM) काफ़ी नहीं है। छोटा मॉडल चुनें या उन्नत में “मेमोरी बचाएँ (int8)” चालू करें।
warn_no_response|⚠ आवाज़ होते हुए भी सबटाइटल आने बंद हो गए। शायद मॉडल सर्वर की ग्राफ़िक्स मेमोरी (VRAM) में नहीं समा रहा: छोटा मॉडल चुनें या उन्नत में “मेमोरी बचाएँ (int8)” चालू करें।
warn_slow_load|⚠ मॉडल लोड होने में बहुत देर लग रही है। शायद वह सर्वर की ग्राफ़िक्स मेमोरी (VRAM) में नहीं समाता: छोटा मॉडल चुनें या उन्नत में “मेमोरी बचाएँ (int8)” चालू करें।
error_reload|पेज फिर से लोड करें (F5) और दोबारा शुरू करें।
error_no_server|पहले सर्वर सेट करें।
settings_title|Stream Transcription · सेटिंग
section_server|सर्वर
section_models|मॉडल
section_subtitles|सबटाइटल
section_interface|इंटरफ़ेस
section_about|परिचय
installed_models|सर्वर पर इंस्टॉल
no_models|अभी कोई मॉडल इंस्टॉल नहीं है।
badge_default|डिफ़ॉल्ट
badge_loaded|मेमोरी में
badge_selected|चुना गया
use_model|इस्तेमाल करें
delete_model|मिटाएँ
confirm_delete|सर्वर से {0} मिटाएँ? इससे {1} खाली होगा।
add_model|मॉडल जोड़ें
add_model_hint|Hugging Face के किसी मॉडल का नाम या लिंक चिपकाएँ। कोई भी Whisper मॉडल चलेगा: faster-whisper (CTranslate2) मॉडल सीधे इस्तेमाल होते हैं और सामान्य (transformers) मॉडल अपने-आप बदल दिए जाते हैं। किसी मॉडल वाली .zip या .tar.gz का सीधा लिंक भी चलेगा।
add_model_placeholder|जैसे Systran/faster-whisper-large-v3
download|डाउनलोड करें
suggestions|सुझाव:
browse_hf|Hugging Face पर Whisper मॉडल देखें
vram_hint|बड़े मॉडल ज़्यादा सटीक हैं पर ज़्यादा ग्राफ़िक्स मेमोरी लेते हैं: small ≈ 1 GB, medium ≈ 2 GB, large ≈ 4 GB।
keep_open|डाउनलोड पूरा होने तक यह पेज खुला रखें।
job_downloading|डाउनलोड हो रहा है… {0} में से {1}
job_downloading_nosize|डाउनलोड हो रहा है… {0}
job_converting|faster-whisper फ़ॉर्मैट में बदला जा रहा है…
job_extracting|खोला जा रहा है…
job_ready|इंस्टॉल हो गया
job_error|विफल: {0}
retry|फिर कोशिश करें
plain_server_hint|यह सामान्य WhisperLive सर्वर है: मॉडल का आकार लिखें (tiny, base, small, medium, large-v3, large-v3-turbo) और सर्वर पहली बार उसे डाउनलोड कर लेगा। यहाँ से कोई भी मॉडल डाउनलोड करने के लिए सर्वर पर Stream Transcription ऐड-ऑन इंस्टॉल करें।
model_name|मॉडल का नाम
save|सेव करें
saved|सेव हो गया
reset_position|सबटाइटल की जगह रीसेट करें
position_reset_done|हो गया: वे फिर नीचे आ जाएँगे।
section_performance|प्रदर्शन
performance_hint|अगर सर्वर के ग्राफ़िक्स कार्ड की मेमोरी कम पड़ जाए (सबटाइटल न आएँ या मेमोरी की चेतावनी दिखे), तो ये दो विकल्प काफ़ी मेमोरी खाली करते हैं। ये सिर्फ़ Stream Transcription सर्वर के साथ काम करते हैं।
precision|मॉडल की सटीकता
precision_auto|अपने-आप
precision_int8|मेमोरी बचाएँ (int8)
precision_hint|int8 लगभग आधी ग्राफ़िक्स मेमोरी लेता है और असल में वही टेक्स्ट लिखता है।
translator_device|अनुवादक कहाँ चलता है
device_gpu|ग्राफ़िक्स कार्ड
device_cpu|प्रोसेसर (CPU)
translator_device_hint|प्रोसेसर पर चलाने से ग्राफ़िक्स मेमोरी खाली होती है, पर अनुवादित सबटाइटल थोड़ा देर से आते हैं।
interface_lang|इंटरफ़ेस की भाषा
lang_auto|ब्राउज़र जैसी
about_text|मुक्त सॉफ़्टवेयर (MIT लाइसेंस)। ऑडियो सिर्फ़ उसी सर्वर पर जाता है जो आप यहाँ सेट करते हैं; और कहीं कुछ नहीं भेजा जाता।
about_based|Collabora के WhisperLive पर आधारित।
source_code|सोर्स कोड
subtitle_preview|आपके सबटाइटल ऐसे दिखेंगे।
err_invalid_source|यह न तो Hugging Face का मॉडल नाम है न लिंक।
err_unsupported_url|सिर्फ़ Hugging Face के लिंक या .zip / .tar.gz फ़ाइलों के सीधे लिंक।
err_repo_not_found|Hugging Face पर यह मॉडल नहीं है (नाम जाँचें)।
err_gated_repo|इस मॉडल के लिए Hugging Face पर शर्तें माननी होती हैं; सर्वर को HF_TOKEN चाहिए।
err_not_whisper|यह Whisper मॉडल नहीं है।
err_no_weights|इस रिपॉज़िटरी में मॉडल के वेट नहीं हैं।
err_network_error|नेटवर्क त्रुटि। फिर कोशिश करें: जहाँ रुका था वहीं से चलेगा।
err_download_failed|डाउनलोड विफल रहा।
err_convert_failed|मॉडल बदला नहीं जा सका।
err_bad_archive|संग्रह फ़ाइल ख़राब है या सुरक्षित नहीं है।
err_already_downloading|यह पहले से डाउनलोड हो रहा है।
err_already_installed|यह पहले से इंस्टॉल है।
err_management_disabled|इस सर्वर पर मॉडल प्रबंधन बंद है।
err_is_default|यह सर्वर का डिफ़ॉल्ट मॉडल है; इसे यहाँ से मिटाया नहीं जा सकता।
err_in_use|चल रहा ट्रांसक्रिप्शन इसे इस्तेमाल कर रहा है।
err_not_found|यह मॉडल अब सर्वर पर नहीं है।
err_server_error|सर्वर त्रुटि।
err_unreachable|सर्वर से कनेक्ट नहीं हो पा रहा।
err_timeout|सर्वर ने समय पर जवाब नहीं दिया।
err_unknown|अनपेक्षित त्रुटि ({0})।
"""
