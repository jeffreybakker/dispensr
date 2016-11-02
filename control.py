import database
import calendar
import time


def get_user(rfid):
	return database.get_user_by_rfid(rfid)


def get_prescriptions(user):
	prescriptions = user.getPrescriptions()

	res = []

	for pres in prescriptions:
		# If the minimum amount of time has not yet passed for the prescription, skip this one

		if pres.last_time + pres.min_time < calendar.timegm(time.gmtime()):
			continue
		elif pres.cur_dose > pres.max_dose:
			continue
		elif pres.duration + pres.pr_date > calendar.timegm(time.gmtime()):
			continue

		inventory = database.get_inventory_by_iid(pres.medicine_id)
		if inventory.stock < pres.amount:
			notify_inventory()
			continue

		pres.last_time = int(calendar.timegm(time.gmtime()))
		pres.cur_dose += 1

		database.update_prescription(pres)

		res.append(pres)

	database.commit()

	return res


def get_inventory():
	return database.get_inventory()


def inventory_refill():
	inventory = get_inventory()

	for i in inventory:
		i.stock = i.capacity
		database.update_inventory(i)

	database.commit()


def notify_inventory():
	pass
