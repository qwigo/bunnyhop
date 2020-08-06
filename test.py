from bunnyhop import Bunny

b = Bunny('<api_key>')
print("Test Billing\n")
print(f"Billing Get: \n {b.Billing.get()}")
print(f"Billing Apply Code: \n {b.Billing.applycode(couponCode='somecode123')}")
print("\nEnd Test Billing\n")
print("Test Purge\n")
print(f"Purge Create: \n {b.Purge.create(url='https://myzone.b-cdn.net/style.css')}")
print("\nEnd Test Purge\n")