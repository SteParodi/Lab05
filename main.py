import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    txt_nuovo_tipo = ft.TextField(label="Tipo", width=160)
    txt_nuova_marca = ft.TextField(label="Marca", width=160)
    txt_nuovo_anno = ft.TextField(label="Anno acquisto", width=140)

    # Campo per visualizzare il valore (gestito con i pulsanti +/-)
    valore_strumento = ft.TextField(value="100", width=80, text_align=ft.TextAlign.RIGHT)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def decrementa_valore(e):
        val = int(valore_strumento.value)
        if val > 0:
            valore_strumento.value = str(val - 10)
            page.update()

    def incrementa_valore(e):
        val = int(valore_strumento.value)
        valore_strumento.value = str(val + 10)
        page.update()

    def aggiungi_nuovo_strumento(e):
        tipo = txt_nuovo_tipo.value.strip()
        marca = txt_nuova_marca.value.strip()
        anno_str = txt_nuovo_anno.value.strip()

        # Controllo campi vuoti
        if tipo == "" or marca == "" or anno_str == "":
            alert.show_alert("Tutti i campi devono essere compilati.")
            return

        # Controllo che l'anno sia un numero
        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("L'anno di acquisto deve essere un numero intero.")
            return

        # Controllo valore
        try:
            valore = float(valore_strumento.value)
        except ValueError:
            alert.show_alert("Il valore deve essere numerico.")
            return

        # Inserimento nel modello dati
        deposito.aggiungi_strumento(tipo, marca, anno, valore)

        # Pulizia dei campi di testo
        txt_nuovo_tipo.value = ""
        txt_nuova_marca.value = ""
        txt_nuovo_anno.value = ""
        valore_strumento.value = "100"

        # Aggiornamento ListView a video
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_meno = ft.IconButton(ft.Icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(ft.Icons.ADD, on_click=incrementa_valore)
    btn_aggiungi_strumento = ft.ElevatedButton("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    # Riga con il contatore (pulsanti - e + con il campo numerico al centro)
    contatore_valore = ft.Row(
        controls=[btn_meno, valore_strumento, btn_piu],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
    )

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(
            controls=[
                txt_nuovo_tipo,
                txt_nuova_marca,
                txt_nuovo_anno,
                contatore_valore,
                btn_aggiungi_strumento
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.run(main)