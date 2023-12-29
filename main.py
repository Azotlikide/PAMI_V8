from case import Case

class MAIN:
    def __init__(self):
        self.Motion=False
        self.Display=True
        self.case = Case(self.Motion, self.Display)

    def run(self):
        while True:
            self.case.MainCase(self.Motion, self.Display)
    


if __name__ == "__main__":
    main = MAIN()
    main.run()
