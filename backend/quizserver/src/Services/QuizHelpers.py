def calculate_quiz_results(quiz, odgovori):
    """
    Zajednička logika za računanje rezultata kviza.
    Može se koristiti i u QuizService i u ProcessWorkers.
    
    Args:
        quiz: Dict sa pitanjima kviza
        odgovori: Lista odgovora igrača
        
    Returns:
        Dict sa rezultatima: {ukupno_bodova, maksimalno_bodova, procenat, tacnih_odgovora}
    """
    ukupno_bodova = 0
    maksimalno_bodova = sum(p["bodovi"] for p in quiz["pitanja"])
    tacnih_odgovora = 0
    
    for pitanje in quiz["pitanja"]:
        igrac_odgovor = next(
            (o for o in odgovori if o["pitanje_id"] == pitanje["id"]), 
            None
        )
        
        if igrac_odgovor:
            tacni_odgovori_ids = [
                odg["id"] for odg in pitanje["odgovori"] if odg.get("tacan", False)
            ]
            
            igrac_odgovor_id = igrac_odgovor.get("odgovor_id")
            igrac_odgovori_ids = igrac_odgovor.get("odgovor_ids", [])
            
            if igrac_odgovor_id:
                igrac_odgovori_ids = [igrac_odgovor_id]
            
            if set(tacni_odgovori_ids) == set(igrac_odgovori_ids):
                ukupno_bodova += pitanje["bodovi"]
                tacnih_odgovora += 1
    
    procenat = round((ukupno_bodova / maksimalno_bodova) * 100, 1) if maksimalno_bodova > 0 else 0.0
    
    return {
        "ukupno_bodova": ukupno_bodova,
        "maksimalno_bodova": maksimalno_bodova,
        "procenat": procenat,
        "tacnih_odgovora": tacnih_odgovora
    }