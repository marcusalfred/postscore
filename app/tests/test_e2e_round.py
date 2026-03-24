"""
End-to-end test: play a full 18-hole round via the API.

Run with -s to see the play-by-play log:
    pytest tests/test_e2e_round.py -v -s
"""
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Course layout: par 72 (4x par-3, 10x par-4, 4x par-5)
# ---------------------------------------------------------------------------
HOLES = [
    {"hole_number": 1,  "par": 4, "yardage": 420, "handicap": 7},
    {"hole_number": 2,  "par": 5, "yardage": 540, "handicap": 11},
    {"hole_number": 3,  "par": 3, "yardage": 175, "handicap": 15},
    {"hole_number": 4,  "par": 4, "yardage": 390, "handicap": 3},
    {"hole_number": 5,  "par": 4, "yardage": 445, "handicap": 1},
    {"hole_number": 6,  "par": 3, "yardage": 160, "handicap": 17},
    {"hole_number": 7,  "par": 5, "yardage": 515, "handicap": 9},
    {"hole_number": 8,  "par": 4, "yardage": 370, "handicap": 13},
    {"hole_number": 9,  "par": 4, "yardage": 405, "handicap": 5},
    {"hole_number": 10, "par": 4, "yardage": 380, "handicap": 6},
    {"hole_number": 11, "par": 5, "yardage": 565, "handicap": 10},
    {"hole_number": 12, "par": 3, "yardage": 155, "handicap": 18},
    {"hole_number": 13, "par": 4, "yardage": 430, "handicap": 2},
    {"hole_number": 14, "par": 4, "yardage": 360, "handicap": 14},
    {"hole_number": 15, "par": 3, "yardage": 190, "handicap": 16},
    {"hole_number": 16, "par": 4, "yardage": 410, "handicap": 4},
    {"hole_number": 17, "par": 5, "yardage": 555, "handicap": 12},
    {"hole_number": 18, "par": 4, "yardage": 450, "handicap": 8},
]

# Scorecard: score, gir, fairway ('o'=hit, '<'=left, '>'=right, None=par-3), putts, penalties
# Total: 79 (+7), 10 GIR, 9/14 fairways, 38 putts, 1 penalty
SCORECARD = [
    #  sc   gir    fw    putts  pen
    (  4,  True,  "o",    2,    0),  # 1  par-4  par
    (  5,  True,  "o",    2,    0),  # 2  par-5  par
    (  3,  True,  None,   2,    0),  # 3  par-3  par
    (  5,  False, "<",    2,    0),  # 4  par-4  bogey
    (  5,  False, "o",    3,    0),  # 5  par-4  bogey
    (  4,  False, None,   2,    0),  # 6  par-3  bogey
    (  4,  True,  "o",    2,    0),  # 7  par-5  birdie
    (  4,  True,  "o",    2,    0),  # 8  par-4  par
    (  5,  False, ">",    3,    0),  # 9  par-4  bogey
    (  4,  True,  "o",    2,    0),  # 10 par-4  par
    (  6,  False, "<",    2,    1),  # 11 par-5  bogey + penalty
    (  3,  True,  None,   1,    0),  # 12 par-3  par (one-putt)
    (  5,  False, ">",    2,    0),  # 13 par-4  bogey
    (  4,  True,  "o",    2,    0),  # 14 par-4  par
    (  4,  False, None,   2,    0),  # 15 par-3  bogey
    (  4,  True,  "o",    2,    0),  # 16 par-4  par
    (  5,  True,  "o",    2,    0),  # 17 par-5  par
    (  5,  False, ">",    3,    0),  # 18 par-4  bogey
]


def _log_section(title: str) -> None:
    logger.info("")
    logger.info("=" * 60)
    logger.info("  %s", title)
    logger.info("=" * 60)


def test_full_round_e2e(client):
    # -----------------------------------------------------------------------
    # 1. Sign up a player
    # -----------------------------------------------------------------------
    _log_section("1. PLAYER SIGNUP")
    signup_resp = client.post("/api/v1/auth/signup", json={
        "name": "Alex Golfer",
        "email": "alex.golfer@example.com",
        "zip": "30301",
        "password": "birdie123",
        "handicap": 6.4,
    })
    assert signup_resp.status_code == 201, signup_resp.text
    player = signup_resp.json()
    logger.info("Player created  id=%s  name=%s  handicap=%s",
                player["id"], player["name"], player.get("handicap"))

    # -----------------------------------------------------------------------
    # 2. Login
    # -----------------------------------------------------------------------
    _log_section("2. LOGIN")
    login_resp = client.post("/api/v1/auth/login",
                             data={"username": "alex.golfer@example.com", "password": "birdie123"})
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    auth = {"Authorization": f"Bearer {token}"}
    logger.info("Login successful  token=%s...", token[:20])

    # -----------------------------------------------------------------------
    # 3. Create a course
    # -----------------------------------------------------------------------
    _log_section("3. CREATE COURSE")
    course_resp = client.post("/api/v1/courses/", json={
        "name": "Pines Golf Club",
        "address": "1 Fairway Dr",
        "city": "Augusta",
        "state": "GA",
        "zip": "30901",
        "website": "https://pinesgolfclub.example.com",
    }, headers=auth)
    assert course_resp.status_code == 201, course_resp.text
    course_id = course_resp.json()["id"]
    logger.info("Course created  id=%s  name=%s", course_id, course_resp.json()["name"])

    # -----------------------------------------------------------------------
    # 4. Add tee boxes (White tees, 18 holes)
    # -----------------------------------------------------------------------
    _log_section("4. ADD TEE BOXES")
    tees_resp = client.post(f"/api/v1/courses/{course_id}/bulk_tees", json=[{
        "tee_box_name": "White",
        "rating": 72.4,
        "slope": 131,
        "yardage": 6683,
        "holes": HOLES,
    }], headers=auth)
    assert tees_resp.status_code == 200, tees_resp.text
    logger.info("Tee boxes added  (%d holes)", len(HOLES))

    # Get tee box + hole IDs
    tee_boxes_resp = client.get(f"/api/v1/courses/{course_id}/tee-boxes", headers=auth)
    assert tee_boxes_resp.status_code == 200, tee_boxes_resp.text
    tee_box = tee_boxes_resp.json()[0]
    tee_box_id = tee_box["id"]
    hole_id_by_number = {h["number"]: h["id"] for h in tee_box["holes"]}
    logger.info("Tee box  id=%s  name=%s  holes=%d",
                tee_box_id, tee_box["name"], len(hole_id_by_number))

    # -----------------------------------------------------------------------
    # 5. Start a round
    # -----------------------------------------------------------------------
    _log_section("5. START ROUND")
    round_resp = client.post("/api/v1/rounds/", json={
        "course_id": course_id,
        "tee_box_id": tee_box_id,
        "holes": 18,
    }, headers=auth)
    assert round_resp.status_code == 201, round_resp.text
    round_id = round_resp.json()["id"]
    logger.info("Round started  id=%s  player_id=%s", round_id, round_resp.json()["player_id"])

    # -----------------------------------------------------------------------
    # 6. Score all 18 holes
    # -----------------------------------------------------------------------
    _log_section("6. SCORING (18 holes)")
    logger.info("%-6s %-5s %-6s %-8s %-6s %-8s", "Hole", "Par", "Score", "To-Par", "GIR", "Fairway")
    logger.info("-" * 45)

    running_total = 0
    running_par = 0

    for hole_data, (score, gir, fairway, putts, penalties) in zip(HOLES, SCORECARD):
        hole_num = hole_data["hole_number"]
        par = hole_data["par"]
        tee_box_hole_id = hole_id_by_number[hole_num]

        payload = {
            "round_id": round_id,
            "tee_box_hole_id": tee_box_hole_id,
            "score": score,
            "gir": gir,
            "putts": putts,
        }
        if fairway is not None:
            payload["fairway"] = fairway
        if penalties:
            payload["penalties"] = penalties

        resp = client.post("/api/v1/rounds/holes", json=payload, headers=auth)
        assert resp.status_code == 201, f"Hole {hole_num} failed: {resp.text}"

        running_total += score
        running_par += par
        diff = score - par
        to_par_str = f"+{diff}" if diff > 0 else str(diff)
        running_str = f"+{running_total - running_par}" if running_total > running_par else str(running_total - running_par)
        fw_display = fairway if fairway else "n/a"

        logger.info("%-6d %-5d %-6d %-8s %-6s %-8s  [running: %s]",
                    hole_num, par, score, to_par_str, "yes" if gir else "no", fw_display, running_str)

    # -----------------------------------------------------------------------
    # 7. Get round with holes
    # -----------------------------------------------------------------------
    _log_section("7. ROUND WITH HOLES")
    round_detail_resp = client.get(f"/api/v1/rounds/{round_id}", headers=auth)
    assert round_detail_resp.status_code == 200, round_detail_resp.text
    round_detail = round_detail_resp.json()
    logger.info("Total score: %s  (holes recorded: %d)",
                round_detail["total_score"], len(round_detail["round_holes"]))

    # -----------------------------------------------------------------------
    # 8. Get round stats
    # -----------------------------------------------------------------------
    _log_section("8. ROUND STATS")
    stats_resp = client.get(f"/api/v1/rounds/{round_id}/stats", headers=auth)
    assert stats_resp.status_code == 200, stats_resp.text
    stats = stats_resp.json()

    to_par_display = f"+{stats['to_par']}" if stats["to_par"] > 0 else str(stats["to_par"])
    logger.info("Score:            %d  (%s)", stats["total_score"], to_par_display)
    logger.info("Par:              %d", stats["par"])
    logger.info("GIR:              %d  (%.1f%%)", stats["greens_in_regulation"], stats["gir_percentage"])
    logger.info("Fairways hit:     %d  (%.1f%%)", stats["fairways_hit"], stats["fairways_percentage"])
    logger.info("Total putts:      %d  (%.1f avg)", stats["total_putts"], stats["avg_putts_per_hole"])
    logger.info("Penalties:        %d", stats["penalties"])

    # -----------------------------------------------------------------------
    # Assertions on final state
    # -----------------------------------------------------------------------
    expected_total = sum(s[0] for s in SCORECARD)  # 78
    expected_par = sum(h["par"] for h in HOLES)     # 72

    assert round_detail["total_score"] == expected_total
    assert len(round_detail["round_holes"]) == 18
    assert stats["total_score"] == expected_total
    assert stats["par"] == expected_par
    assert stats["to_par"] == expected_total - expected_par

    expected_gir = sum(1 for s in SCORECARD if s[1])
    assert stats["greens_in_regulation"] == expected_gir

    non_par3_count = sum(1 for h in HOLES if h["par"] != 3)
    expected_fw = sum(1 for h, s in zip(HOLES, SCORECARD) if h["par"] != 3 and s[2] == "o")
    assert stats["fairways_hit"] == expected_fw
    assert stats["fairways_percentage"] == round(expected_fw / non_par3_count * 100, 1)

    expected_putts = sum(s[3] for s in SCORECARD)
    assert stats["total_putts"] == expected_putts
    assert stats["avg_putts_per_hole"] == round(expected_putts / 18, 1)

    expected_penalties = sum(s[4] for s in SCORECARD)
    assert stats["penalties"] == expected_penalties

    _log_section("ROUND COMPLETE")
    logger.info("All assertions passed.")
