import frappe
from frappe.model.document import Document
from frappe.utils import flt

class RealEstateUnit(Document):
	def validate(self):
		self.total_installment = flt(self.down_payment) + flt(self.remaining_installment)
		self.remaining_to_pay = flt(self.price) - flt(self.down_payment)

	def onload(self):
		if self.is_new():
			return

		views = flt(self.views_count) + 1
		self.views_count = views
		frappe.db.set_value(self.doctype, self.name, "views_count", views, update_modified=False)
