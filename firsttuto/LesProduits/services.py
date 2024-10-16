from threading import Timer
from .models import Commande

class CommandeTimerService:
    def __init__(self, commande_id):
        self.commande_id = commande_id
        self.timer = None

    def advance_status(self):
        commande = Commande.objects.get(id=self.commande_id)
        if commande.status < 2:
            commande.status += 1
            commande.save()
            if commande.status < 2:
                self.start_status_timer()

    def start_status_timer(self):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(20.0, self.advance_status)
        self.timer.start()

    def reset_status_timer(self):
        commande = Commande.objects.get(id=self.commande_id)
        if commande.status == 0:
            self.start_status_timer()
        elif self.timer:
            self.timer.cancel()
            self.timer = None