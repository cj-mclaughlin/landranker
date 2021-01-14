# Managing of Land ELO Updates
from storageservice import query_land_objects, update_land_elo, add_match_result
k_factor = 20

def process_match_results(land_id1, land_id2, result):
	"""
	Update DB after result of a land match

	Args:
		land_id1: integer id of land value for match
		land_id2: integer id of land value for match
		result: boolean true if land1 wins, false if land2

	Returns:
		StatusCode
	"""
	try:
		land1, land2 = query_land_objects(land_id1, land_id2)
		delta_r1, delta_r2 = calculate_elo_changes(land1["elo"], land2["elo"], result)
		update_land_elo(land1["land_id"], land1["elo"] + delta_r1)
		update_land_elo(land2["land_id"], land1["elo"] + delta_r2)
		add_match_result(land_id1, land_id2, result)
		return 200
	except:
		return 400


def calculate_elo_changes(R1, R2, result):
	"""
	Calulate ELO changes for each land given match data

	Args:
		R1: integer pre-match elo of land1
		R2: integer pre-match elo of land2
		result: boolean true if land1 wins, false if land2

	Returns:
		Tuple of elo changes to each land
	"""
	e_l1 = calculate_e_l1(R1, R2)
	e_l2 = 1 - e_l1
	l1_win, l2_win = 1 if result else 0, 0 if result else 1 
	delta_r1 = k_factor * (l1_win - e_l1)
	delta_r2 = k_factor * (l2_win - e_l2)
	return (delta_r1, delta_r2)


def calculate_e_l1(R1, R2):
	"""
	Calculate expected probability of land1 winning based on elo ratings

	Args:
		R1: integer pre-match elo of land1
		R2: integer pre-match elo of land2

	Returns:
		Float win probability of land1
	"""
	e_l1 = 1 / (1 + 10**((R2 - R1)/400))
	return e_l1