# from flask import Flask, render_template, request, session
# import secrets
# import os
# from dotenv import load_dotenv


# load_dotenv()


# app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')


# def calcola_certificato_corretto(data):
#     try:
#         prezzo_iniziale = float(data.get('prezzo_iniziale', 0))
#         valore_finale = float(data.get('valore_finale', 0))
#         tipo_input = data.get('tipo_input', 'prezzo')
#         tipo = data.get('tipo', 'long')
#         leva = float(data.get('leva', 1))
#         barriera_ko = float(data.get('barriera_ko', 0))
#         quantita = int(data.get('quantita', 0))
#         prezzo_pagato = float(data.get('prezzo_pagato', 0))
#         commissioni = float(data.get('commissioni', 0))
#         tasse_percent = float(data.get('tasse', 26))
        
#         # Calcola prezzo finale e variazione
#         if tipo_input == 'percentuale':
#             variazione_percent = valore_finale
#             prezzo_finale = prezzo_iniziale * (1 + variazione_percent / 100)
#         else:
#             prezzo_finale = valore_finale
#             variazione_percent = ((prezzo_finale - prezzo_iniziale) / prezzo_iniziale) * 100
        
#         # Verifica KO
#         ko_attivato = False
#         if tipo == "long" and prezzo_finale <= barriera_ko:
#             ko_attivato = True
#         elif tipo == "short" and prezzo_finale >= barriera_ko:
#             ko_attivato = True
        
#         # Calcolo semplificato del prezzo certificato
#         if ko_attivato:
#             prezzo_cert_teorico = 0
#         else:
#             # Movimento del certificato basato sulla variazione del sottostante
#             if tipo == "long":
#                 movimento_cert_percent = variazione_percent * leva
#             else:  # short
#                 movimento_cert_percent = -variazione_percent * leva
            
#             # Il certificato si muove partendo dal prezzo che hai pagato
#             prezzo_cert_teorico = prezzo_pagato * (1 + movimento_cert_percent / 100)
#             prezzo_cert_teorico = max(0, prezzo_cert_teorico)  # Non può essere negativo
        
#         # Calcoli finanziari
#         investimento_totale = quantita * prezzo_pagato
#         valore_attuale = quantita * prezzo_cert_teorico
#         guadagno_lordo = valore_attuale - investimento_totale
#         guadagno_dopo_commissioni = guadagno_lordo - commissioni
        
#         # Tasse solo sui guadagni
#         if guadagno_dopo_commissioni > 0:
#             tasse_pagate = guadagno_dopo_commissioni * (tasse_percent / 100)
#             guadagno_netto = guadagno_dopo_commissioni - tasse_pagate
#         else:
#             tasse_pagate = 0
#             guadagno_netto = guadagno_dopo_commissioni
        
#         # Rendimento percentuale
#         if investimento_totale > 0:
#             rendimento_percent = (guadagno_netto / investimento_totale) * 100
#         else:
#             rendimento_percent = 0
        
#         return {
#             'prezzo_iniziale': prezzo_iniziale,
#             'prezzo_finale': round(prezzo_finale, 2),
#             'variazione_percent': round(variazione_percent, 2),
#             'tipo': tipo.upper(),
#             'leva': leva,
#             'barriera_ko': barriera_ko,
#             'ko_attivato': ko_attivato,
#             'prezzo_cert_teorico': round(prezzo_cert_teorico, 3),
#             'investimento_totale': round(investimento_totale, 2),
#             'valore_attuale': round(valore_attuale, 2),
#             'commissioni': commissioni,
#             'tasse_pagate': round(tasse_pagate, 2),
#             'guadagno_netto': round(guadagno_netto, 2),
#             'rendimento_percent': round(rendimento_percent, 2)
#         }
        
#     except Exception as e:
#         return {'errore': f"Errore: {str(e)}"}

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         session['result1'] = None
#         session['result2'] = None
    
#     if request.method == 'POST':
#         if 'submit1' in request.form:
#             session ['result1'] = calcola_certificato_corretto(request.form)
#             if 'result2' in session:
#                 result2 = session['result2']
#             else:
#                 result2 = None
#             return render_template('index.html', result1=session['result1'], result2=result2)

#         elif 'submit2' in request.form:
#             # Rimuovi prefisso "2_"
#             form_data = {}
#             for key, value in request.form.items():
#                 if key.startswith('2_'):
#                     form_data[key[2:]] = value
#                 else:
#                     form_data[key] = value
#             session ['result2'] = calcola_certificato_corretto(form_data)
#             if 'result1' in session:
#                 result1 = session['result1']
#             else: 
#                 result1 = None
    
#             return render_template('index.html', result1=result1, result2=session['result2'])
        
#     return render_template('index.html', result1=session.get('result1'), result2=session.get('result2'))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, render_template, request, session
import secrets
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


def calcola_certificato_corretto(data):
    try:
        prezzo_iniziale = float(data.get('prezzo_iniziale', 0))
        valore_finale = float(data.get('valore_finale', 0))
        tipo_input = data.get('tipo_input', 'prezzo')
        tipo = data.get('tipo', 'long')
        barriera_ko = float(data.get('barriera_ko', 0))
        quantita = int(data.get('quantita', 0))
        commissioni = float(data.get('commissioni', 0))
        tasse_percent = float(data.get('tasse', 26))
        
        # NUOVI CAMPI CON FORMULE UFFICIALI SG
        multiplo = float(data.get('ratio', 0.05))  # Il "ratio" di TR è il "Multiplo" di SG
        tipo_acquisto = data.get('tipo_acquisto', 'prezzo_cert')
        valore_acquisto = float(data.get('valore_acquisto', 0))
        tasso_cambio = float(data.get('tasso_cambio', 1.0))  # Default 1 se stessa valuta
        
        # Calcola prezzo finale e variazione del sottostante
        if tipo_input == 'percentuale':
            variazione_percent = valore_finale
            prezzo_finale = prezzo_iniziale * (1 + variazione_percent / 100)
        else:
            prezzo_finale = valore_finale
            variazione_percent = ((prezzo_finale - prezzo_iniziale) / prezzo_iniziale) * 100
        
        # FORMULE UFFICIALI SG: Strike = Barriera nei Turbo
        strike = barriera_ko
        
        # Calcola prezzo sottostante all'acquisto e prezzo certificato all'acquisto
        # usando le formule inverse di SG
        if tipo_acquisto == 'prezzo_cert':
            # Ho il prezzo del certificato, calcolo il prezzo del sottostante all'acquisto
            prezzo_cert_acquisto = valore_acquisto
            if tipo == "long":
                # Valore_intrinseco = (Sottostante_acquisto - Strike) × Multiplo ÷ Tasso_cambio
                # Quindi: Sottostante_acquisto = (Valore_intrinseco × Tasso_cambio ÷ Multiplo) + Strike
                prezzo_sotto_acquisto = (prezzo_cert_acquisto * tasso_cambio / multiplo) + strike
            else:  # short
                # Valore_intrinseco = (Strike - Sottostante_acquisto) × Multiplo ÷ Tasso_cambio  
                # Quindi: Sottostante_acquisto = Strike - (Valore_intrinseco × Tasso_cambio ÷ Multiplo)
                prezzo_sotto_acquisto = strike - (prezzo_cert_acquisto * tasso_cambio / multiplo)
        else:
            # Ho il prezzo del sottostante all'acquisto, calcolo il prezzo del certificato
            prezzo_sotto_acquisto = valore_acquisto
            if tipo == "long":
                # Valore_intrinseco = (Sottostante_acquisto - Strike) × Multiplo ÷ Tasso_cambio
                prezzo_cert_acquisto = (prezzo_sotto_acquisto - strike) * multiplo / tasso_cambio
            else:  # short
                # Valore_intrinseco = (Strike - Sottostante_acquisto) × Multiplo ÷ Tasso_cambio
                prezzo_cert_acquisto = (strike - prezzo_sotto_acquisto) * multiplo / tasso_cambio
        
        # Verifica KO usando le regole SG
        ko_attivato = False
        if tipo == "long" and prezzo_finale <= barriera_ko:
            ko_attivato = True
        elif tipo == "short" and prezzo_finale >= barriera_ko:
            ko_attivato = True
        
        # Calcolo del prezzo certificato attuale usando FORMULE UFFICIALI SG
        if ko_attivato:
            prezzo_cert_teorico = 0
            leva_dinamica = 0
        else:
            if tipo == "long":
                # Formula SG TURBO LONG: (Valore_Sottostante - Strike) × Multiplo ÷ Tasso_cambio
                prezzo_cert_teorico = (prezzo_finale - strike) * multiplo / tasso_cambio
            else:  # short
                # Formula SG TURBO SHORT: (Strike - Valore_Sottostante) × Multiplo ÷ Tasso_cambio
                prezzo_cert_teorico = (strike - prezzo_finale) * multiplo / tasso_cambio
            
            prezzo_cert_teorico = max(0, prezzo_cert_teorico)  # Non può essere negativo
            
            # Calcolo LEVA DINAMICA usando formula ufficiale SG
            # Leva = (Valore_Sottostante × Multiplo) ÷ (Prezzo_Certificato × Tasso_cambio)
            if prezzo_cert_teorico > 0:
                leva_dinamica = (prezzo_finale * multiplo) / (prezzo_cert_teorico * tasso_cambio)
            else:
                leva_dinamica = 0
        
        # Calcoli finanziari
        investimento_totale = quantita * prezzo_cert_acquisto
        valore_attuale = quantita * prezzo_cert_teorico
        guadagno_lordo = valore_attuale - investimento_totale
        guadagno_dopo_commissioni = guadagno_lordo - commissioni
        
        # Tasse solo sui guadagni
        if guadagno_dopo_commissioni > 0:
            tasse_pagate = guadagno_dopo_commissioni * (tasse_percent / 100)
            guadagno_netto = guadagno_dopo_commissioni - tasse_pagate
        else:
            tasse_pagate = 0
            guadagno_netto = guadagno_dopo_commissioni
        
        # Rendimento percentuale
        if investimento_totale > 0:
            rendimento_percent = (guadagno_netto / investimento_totale) * 100
        else:
            rendimento_percent = 0
        
        return {
            'prezzo_iniziale': prezzo_iniziale,
            'prezzo_finale': round(prezzo_finale, 2),
            'variazione_percent': round(variazione_percent, 2),
            'tipo': tipo.upper(),
            'multiplo': multiplo,
            'strike': strike,
            'barriera_ko': barriera_ko,
            'ko_attivato': ko_attivato,
            'leva_dinamica': round(leva_dinamica, 2),
            'prezzo_sotto_acquisto': round(prezzo_sotto_acquisto, 2),
            'prezzo_cert_acquisto': round(prezzo_cert_acquisto, 3),
            'prezzo_cert_teorico': round(prezzo_cert_teorico, 3),
            'investimento_totale': round(investimento_totale, 2),
            'valore_attuale': round(valore_attuale, 2),
            'commissioni': commissioni,
            'tasse_pagate': round(tasse_pagate, 2),
            'guadagno_netto': round(guadagno_netto, 2),
            'rendimento_percent': round(rendimento_percent, 2)
        }
        
    except Exception as e:
        return {'errore': f"Errore: {str(e)}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session['result1'] = None
        session['result2'] = None
    
    if request.method == 'POST':
        if 'submit1' in request.form:
            session ['result1'] = calcola_certificato_corretto(request.form)
            if 'result2' in session:
                result2 = session['result2']
            else:
                result2 = None
            return render_template('index.html', result1=session['result1'], result2=result2)

        elif 'submit2' in request.form:
            # Rimuovi prefisso "2_"
            form_data = {}
            for key, value in request.form.items():
                if key.startswith('2_'):
                    form_data[key[2:]] = value
                else:
                    form_data[key] = value
            session ['result2'] = calcola_certificato_corretto(form_data)
            if 'result1' in session:
                result1 = session['result1']
            else: 
                result1 = None
    
            return render_template('index.html', result1=result1, result2=session['result2'])
        
    return render_template('index.html', result1=session.get('result1'), result2=session.get('result2'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)