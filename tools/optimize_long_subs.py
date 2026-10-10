import json
import os

def run():
    base_proj = r"E:\MisApps\Reverse\doom3phobos"
    subs_path = os.path.join(base_proj, "translated_subtitles.json")
    long_path = os.path.join(base_proj, "tools", "long_subs_to_fix.json")

    with open(subs_path, "r", encoding="utf-8") as f:
        subs = json.load(f)

    with open(long_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    replacements = {
        0: "Pronóstico para Marte City mañana, 16 de noviembre de 2145.\nMayormente despejado. Temperaturas de -120 °C.",
        1: "Investigación federal en curso.\nPor la seguridad de todos, mantengan la calma y cooperen.",
        2: "Lo siento amigo. Este camino está bloqueado.\nUn idiota puso estas cajas aquí y trato de ver adónde van.",
        3: "Lo siento, el monorraíl está muy voluble.\nYa están trabajando en ello, pero no puedo dejarte entrar, amigo.",
        4: "No puedo dejarte entrar. Pero el monorraíl ya funciona;\nes la única forma de desplazarte ahora mismo.",
        5: "Estás de suerte amigo. El monorraíl volvió a funcionar.\nNo todas las líneas van, pero este llegará enseguida.",
        6: "No sé qué pasa con los temblores, nadie nos dice nada.\nSupongo que ustedes los federales son muy reservados.",
        7: "Robaron nuestros estados en el viejo planeta.\nPero en esta estación, en este planeta: No. Son. Bienvenidos.",
        8: "¿Cuándo es suficiente? ¿Tienen que adueñarse de todo?\nMalditos federales, siempre husmeando donde no deben.",
        9: "¡Oye, tú! Zona restringida. Evaluamos la situación,\nasí que el Comando de Marines está cerrado.",
        10: "Estará ocupada un rato. Pero puedes alcanzarla en la\nTerminal de Aterrizaje, cruzando el vestíbulo.",
        11: "Las enfermeras ya la habían trasladado; yo no estaba allí.\nFue como si ella nunca hubiera estado allí.",
        12: "Sospechamos que la polémica con los laboratorios Delta de\nla UAC ha jugado un papel muy importante.",
        13: "La corporación es el vivo ejemplo de la codicia y el desprecio\ntotal por la seguridad y la libertad personal.",
        14: "Transmisión de emergencia. Esto no es un simulacro.\nLas siguientes instrucciones son vitales para su seguridad.",
        15: "Quien esté cerca de la Terminal de Aterrizaje de Mars City\ndebe acudir de inmediato para su evacuación.",
        16: "Agente Simmons llamando a Jim Benson. Responda a la radio.\nVenga de inmediato, no vamos a esperar.",
        17: "Agente Benson, listos para despegar. Si escucha esto,\nvaya al Baluarte usando las líneas de combustible.",
        18: "Mencionaste tuberías. Sé con certeza que el Baluarte tiene\nuna línea que sube directo a su plataforma.",
        19: "Supongo que conecta con la estación de combustible principal,\ny la Terminal donde estás también lo hace.",
        20: "Cuando los federales tomaron el transbordador, llamaron\na un tal Benson para que usara las tuberías.",
        21: "¿Escapar? ¡No! Se largaron y nos dejaron tirados.\nLa tripulación murió. Creí que conocías a estos tipos.",
        22: "Lo conocí en la academia. Es un agente federal como Calloway\ny yo. Tuvo un problema con él hace unos años.",
        23: "Tomó algo demasiado hermoso y lo convirtió en cenizas.\nTraicionó nuestra confianza y se volvió contra nosotros.",
        24: "Pensé que debíamos separarnos y revisar varias rutas para\nestar seguros. Yo elegí los conductos.",
        25: "Me dijiste que buscaste una eternidad en los pasillos del\nHospital St. Amber, como atrapada para siempre.",
        26: "Llevamos mucho tiempo en esto, pero piensa en lo bien que la\npasamos en el valle. ¿De verdad estamos tan mal?",
        27: "Lo que digo es... si este intento falla, ¿debemos seguir?\nSiento como si estuviéramos huyendo...",
        28: "Mi padre dejó de existir cuando murió mi madre;\nen realidad, en las últimas dos semanas de su vida.",
        29: "¿Recuerdas mi campamento con él el otoño pasado?\nNo fue un campamento, fue otro viaje a la clínica.",
        30: "Lo siento. Pero el valle es grande, ¿no podemos buscar\notro sitio? ¿Tiene que ser fuera de los muros?",
        31: "Los registros oficiales dicen que Kaylee murió en el incendio,\nidentificada por ADN, como ambos sabemos.",
        32: "Los incendios comunes no se acordonan con soldados,\ncientíficos con trajes NBQ y altos mandos alertados.",
        33: "No tengo acceso a los archivos federales, pero conocer a la\ngente adecuada y un poco de astucia ayudan mucho.",
        34: "Creo que me vigilan y me queda poco tiempo aquí.\nPor eso recurro a ti. Por Kaylee.",
        35: "Sé que es mucho que asimilar tras tantos años, pero necesito\ntu ayuda. ¡Ven al Baluarte, Samantha, rápido!",
        36: "Sé que todo esto es muy confuso, pero no nos precipitemos.\nNo puedo irme porque tengo deberes que cumplir.",
        37: "Cálmate. Conozco a Calloway hace tiempo, somos amigos.\nEn la Tierra perdimos a alguien muy cercano.",
        38: "Mi único contacto aquí es un sargento de voz suave\nque bien podría ser un robot...",
        39: "¿Qué? No. Iba en la dirección correcta y luego todo se desvió.\nEstoy atrapado en una línea de carga.",
        40: "¡Sí, salió genial! Vamos, yo hago el trabajo duro,\nnadando en combustible y en plataformas. ¿Qué te importa?",
        41: "Ah, claro, qué tonto. La pantalla está apagada. ¿La enciendes?\nDebe estar junto al comunicador.",
        42: "Comía por un tubo. Si la morfina no la calmaba, sufría dolor.\nEstaba atrapada en su propia mente.",
        43: "Papá casi nunca estaba. Mi hermano no la visitaba.\nElla solo yacía en la cama, mirándome.",
        44: "Pero cada día venía el personal médico. Vi exactamente qué\nle daban para el dolor y cómo lo hacían.",
        45: "60 mg de morfina, 4 veces al día. A veces me sentaba allí,\ndeseando que le dieran más para terminar con todo.",
        46: "Al día siguiente tras sus inyecciones, me colé en el almacén\ny conseguí una dosis extra.",
        47: "Vi cómo la vida dejaba sus ojos. Se desvaneció en la nada\nantes de que comprendiera lo que había hecho.",
        48: "¿Una tubería hacia el Baluarte? La encontré unos pasos atrás.\nEstá destruida. Infranqueable.",
        49: "En una sala de comunicaciones, cerca de... bueno, la verdad\nya no estoy seguro a estas alturas.",
        50: "¿Me das el CMID? Es el identificador de cada sala de radio.\nEmpieza con 'CM-'.",
        51: "Le preguntas quién eres, te tomas algo y descansas seguro\ntras los muros fortificados. Obviamente.",
        52: "Solo te pido que me contactes y me digas que está a salvo,\naunque debas cruzar esos muros. Por favor.",
        53: "Al caer la oscuridad y dejarte ir, el tiempo se estira hacia el\ninfinito, dejándote en un estado eterno.",
        54: "Tus recuerdos se distorsionarían y los que amabas se borrarían,\nquedando solo como ecos en tu mente.",
        55: "Es como ahogarse. Tu cuerpo se enfría y entumece con el agua.\nNo flotas; te hundes como una piedra.",
        56: "Pero no es asunto mío. La verdad es que quieres escapar,\ny ya he ayudado a otros a lograrlo antes.",
        57: "Acabarás de vuelta en territorio federal porque no queda\nningún otro lugar adonde ir en este planeta.",
        58: "Si decides buscar mi ayuda, estaré en este apartamento toda la\nsemana. Después de eso, me marcho.",
        59: "Sé que puedo ayudarte. Entra y llama a mi habitación,\nes la número 10. Usa el teléfono del motel.",
        60: "Por más que intentaba fijarme en árboles o torres de agua,\nsiempre desaparecían en el horizonte.",
        61: "Salir de una zona federal es muy delicado ahora.\nPero puedo llevarte a cualquier punto de la zona.",
        62: "¿Por qué llamas? Estoy ocupado. Ve por la chica,\nhabla con ella y mueve las cosas. ¿A qué esperas?",
        63: "Lo aprecio, pero si todo falla la caja es nuestra baza.\n¡Podemos hacerlo y debemos hacerlo!",
        64: "Como sospechábamos, la caja es nuestro pasaje de salida;\ny aquí es donde nuestro vecino Karl puede ayudar.",
        65: "Podrías probar la puerta principal o la del garaje,\npero seguro que están cerradas.",
        66: "Con la caja, toma el autobús hasta nuestro refugio.\nEscóndela en el lugar seguro y espérame allí.",
        67: "Al final del día, tendremos la caja en el granero\ny podremos seguir adelante con nuestras vidas.",
        68: "Quizá tuvieron que replegarse más en el complejo.\nNo es tan seguro como creíamos.",
        69: "Casi todo el personal volvió a Fobos para asegurar activos\nimportantes. Soy parte de ese grupo.",
        70: "¿Familia enferma, perder el trabajo, desamores?\n¿De verdad necesitas toda esa carga encima?",
        71: "Marte y sus lunas albergaron una gran civilización,\nconocida comúnmente como 'Los Antiguos'.",
        72: "Sus avances científicos dieron grandes resultados al\nrevelar la existencia de dos dimensiones más.",
        73: "Un gran filtro destinado a destruir su civilización\no retrasarla al menos miles de años.",
        74: "Se sabe poco de la unión entre ambos reinos,\npero suponemos que existe un paso intermedio.",
        75: "El artefacto fue hallado bajo la corteza de Marte,\nsiendo un hallazgo histórico prioritario.",
        76: "Se envió de inmediato a los mejores científicos\ny arqueólogos que la humanidad puede ofrecer.",
        77: "Interrumpiendo su estudio, el artefacto fue robado\ny desapareció casi durante una década entera.",
        78: "Tras una ardua investigación, se recuperó en la Tierra\ny volvió a su dueño: la gloriosa federación.",
        79: "Pese al esfuerzo de los mejores en su campo, la función\ny propósito del artefacto siguen siendo un misterio.",
        80: "Las pruebas indican que usa una energía invisible,\ncon un brillo pulsante y temperatura constante.",
        81: "Investigadores notan su gran parecido con las propiedades\ndel receptáculo hallado en Fobos.",
        82: "Nuestra moderna instalación protege el más increíble\nde nuestros descubrimientos: el receptáculo.",
        83: "Tablillas y textos antiguos revelan que se trata\nde una especie de portal a otra dimensión.",
        84: "Hubo más suerte con materiales inorgánicos que\naparecieron en una estación de escucha en Marte.",
        85: "El área de la estación de escucha era al principio un\napartamento común de obreros de la UAC en Marte.",
        86: "Hoy es vanguardia de investigación científica,\nestando íntimamente ligada al receptáculo.",
        87: "¿Una celda cerrada no sería lo más seguro en este caso?\nQuizá no esté tan mal después de todo."
    }

    # Validate all lengths
    for idx, new_val in replacements.items():
        if len(new_val) > 120:
            print(f"ERROR: {idx} is too long ({len(new_val)} chars)")
            return

    # Apply to subs
    applied = 0
    for idx, (orig_en, old_es) in enumerate(items):
        if idx in replacements:
            subs[orig_en] = replacements[idx]
            applied += 1

    # Check whole subs dictionary
    max_len = 0
    over_limit = []
    for k, v in subs.items():
        if len(v) > max_len:
            max_len = len(v)
        if len(v) > 120:
            over_limit.append((k, v, len(v)))

    print(f"Applied {applied} replacements successfully.")
    print(f"Max subtitle length across entire game: {max_len}")
    if over_limit:
        print(f"WARNING: {len(over_limit)} subtitles still > 120 chars!")
        for k, v, l in over_limit:
            print(f"  [{l}] {repr(v[:60])}...")
    else:
        print("ALL subtitles are now <= 120 characters!")

    with open(subs_path, "w", encoding="utf-8") as f:
        json.dump(subs, f, indent=2, ensure_ascii=False)
    print(f"Updated {subs_path}")

if __name__ == "__main__":
    run()

