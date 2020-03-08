from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

class Country:
    def __init__(self, population, disease):
        self.population = population
        self.infected = [0 for _ in range(disease.sick_time)]
        self.resistant = 0
        self.dead = 0
        self.disease = disease

    def infect(self, amount):
        self.infected[0] += amount
        self.resistant += amount

    def day(self):
        self.disease.run(self)

    def alive_population(self):
        return self.population-self.dead

    def total_infected(self):
        return sum(self.infected)

    def reported_invected(self):
        return sum(self.infected[len(self.infected)//2:])


class Disease:
    def __init__(self, sick_time, ineffectiveness, mortality):
        self.sick_time = sick_time
        self.ineffectiveness = ineffectiveness
        self.per_day_chance = ineffectiveness/sick_time
        self.mortality = mortality

    def run(self, country):
        un_risistant_fraction = (country.alive_population()-country.resistant)/country.alive_population()
        new_sick = country.total_infected()*self.per_day_chance*un_risistant_fraction
        country.infected = [new_sick]+country.infected[0:-1]
        country.resistant += new_sick

        deads = country.total_infected()*self.mortality/self.sick_time
        country.dead += deads
        country.resistant -= deads

        p = len(country.infected)-1

        while deads>0:
            diff = deads - country.infected[p]
            if diff > 0:
                country.infected[p] = 0
                deads = diff
                p-=1
            else:
                country.infected[p] -= deads
                deads = 0


if __name__ == '__main__':
    # Test simulation
    covid_19 = Disease(20,2,0.02)
    netherlands = Country(17e6,covid_19)

    sick_hist = []
    dead_hist = []
    reported_hist = []

    for _ in range(10):
        sick_hist.append(netherlands.total_infected())
        dead_hist.append(netherlands.dead)
        reported_hist.append(netherlands.reported_invected())
        netherlands.day()
        netherlands.infect(10)


    for _ in range(400):
        sick_hist.append(netherlands.total_infected())
        dead_hist.append(netherlands.dead)
        reported_hist.append(netherlands.reported_invected())
        netherlands.day()
    sick_hist.append(netherlands.total_infected())
    dead_hist.append(netherlands.dead)
    reported_hist.append(netherlands.reported_invected())

    plt.plot(sick_hist)
    plt.plot(dead_hist)
    plt.plot(reported_hist)
plt.show()