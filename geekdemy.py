from abc import ABC, abstractmethod

# Store programs as list of dictionaries for better management
programs = []  # Each item: {'name': str, 'unit_price': float, 'count': int, 'total_price': float}

class Programmes(ABC):
    @abstractmethod
    def programmes(self):
        pass

class Certification(Programmes):
    @staticmethod
    def programmes():
        program = 'certification'
        unit_price = 3000.0
        try:
            count = int(input("\nCOUNT OF CERTIFICATION PROGRAMMES NEEDED?:\t"))
            if count <= 0:
                raise ValueError("Count must be positive.")
            total_price = count * unit_price
            programs.append({'name': program, 'unit_price': unit_price, 'count': count, 'total_price': total_price})
            return total_price, count
        except ValueError as e:
            print(f"\nINVALID INPUT: {e}\n")
            return Certification.programmes()

class Degree(Programmes):
    @staticmethod
    def programmes():
        program = 'degree'
        unit_price = 5000.0
        try:
            count = int(input("\nCOUNT OF DEGREE PROGRAMMES NEEDED?:\t"))
            if count <= 0:
                raise ValueError("Count must be positive.")
            total_price = count * unit_price
            programs.append({'name': program, 'unit_price': unit_price, 'count': count, 'total_price': total_price})
            return total_price, count
        except ValueError as e:
            print(f"\nINVALID INPUT: {e}\n")
            return Degree.programmes()

class Diploma(Programmes):
    @staticmethod
    def programmes():
        program = 'diploma'
        unit_price = 2500.0
        try:
            count = int(input("\nCOUNT OF DIPLOMA PROGRAMMES NEEDED?:\t"))
            if count <= 0:
                raise ValueError("Count must be positive.")
            total_price = count * unit_price
            programs.append({'name': program, 'unit_price': unit_price, 'count': count, 'total_price': total_price})
            return total_price, count
        except ValueError as e:
            print(f"\nINVALID INPUT: {e}\n")
            return Diploma.programmes()

class Cupons(ABC):
    @abstractmethod
    def cupons(self, total_cost, total_count):
        pass

class B4G1(Cupons):
    def cupons(self, total_cost, total_count):
        if total_count >= 4:
            # Find the program with the lowest total price
            free_program = min(programs, key=lambda x: x['total_price'])
            discount = free_program['unit_price']  # Free one program
            print(f"\nCOUPON B4G1 ACTIVATED:\nYOU GET 1 FREE PROGRAM: {free_program['name'].capitalize()} (₹{discount})")
            return discount, 'B4G1'
        else:
            print("COUPON B4G1 NOT APPLIED")
            return 0, 'DISCOUNT_NONE'

class Deal_G20(Cupons):
    def cupons(self, total_cost, _):
        if total_cost >= 10000:
            discount = total_cost * 0.20
            print(f"\nDEAL_G20 ACTIVATED:\n20% DISCOUNT APPLIED: ₹{discount:.2f}")
            return discount, 'DEAL_G20'
        else:
            print("COUPON DEAL_G20 NOT ELIGIBLE")
            return 0, 'DISCOUNT_NONE'

class Deal_G5(Cupons):
    def cupons(self, total_cost, total_count):
        if total_count >= 2:
            discount = total_cost * 0.05
            print(f"\nDEAL_G5 ACTIVATED:\n5% DISCOUNT APPLIED: ₹{discount:.2f}")
            return discount, 'DEAL_G5'
        else:
            print("COUPON DEAL_G5 NOT APPLICABLE")
            return 0, 'DISCOUNT_NONE'

class Pro_Membership_fee:
    def check_membership_fee(self):
        membership = input("DO YOU WANT TO TAKE MEMBERSHIP (₹200)? (y/n):\t").strip().lower()
        total_pro_discount = 0
        membership_fee = 200 if membership == 'y' else 0

        if membership == 'y':
            print("\nPRO MEMBERSHIP APPLIED: ₹200")
            for program in programs:
                if program['name'] == 'certification':
                    discount = program['total_price'] * 0.02  # 2%
                elif program['name'] == 'degree':
                    discount = program['total_price'] * 0.03  # 3%
                elif program['name'] == 'diploma':
                    discount = program['total_price'] * 0.01  # 1%
                else:
                    discount = 0
                program['total_price'] -= discount
                total_pro_discount += discount
                print(f"Pro Membership Discount for {program['name'].capitalize()}: ₹{discount:.2f}")
        else:
            print("\nNO PRO MEMBERSHIP APPLIED")

        return total_pro_discount, membership_fee

class EnrollmentFee:
    @staticmethod
    def apply_enrollment_fee(total_cost):
        enrollment_fee = 0
        if total_cost < 6666:
            enrollment_fee = 500
            print("\nENROLLMENT FEE OF ₹500 APPLIED")
        else:
            print("\nENROLLMENT FEE WAIVED")
        return enrollment_fee

class Geekdemy:
    total_program_count = 0

    @staticmethod
    def geekdemy():
        print("\n\t\tWELCOME TO GEEKDEMY\n")
        Geekdemy.select_programmes()

    @staticmethod
    def select_programmes():
        while True:
            program = input("\nENTER THE PROGRAM YOU WANT TO PURCHASE (certification, degree, diploma) or 'done' to finish:\t").strip().lower()
            if program == 'done':
                if not programs:
                    print("\nNO PROGRAMS SELECTED\n")
                    Geekdemy.exit_geekdemy()
                else:
                    break
            elif program in ['certification', 'degree', 'diploma']:
                if program == 'certification':
                    _, count = Certification.programmes()
                elif program == 'degree':
                    _, count = Degree.programmes()
                elif program == 'diploma':
                    _, count = Diploma.programmes()
                Geekdemy.total_program_count += count
            else:
                print("\nINVALID PROGRAM. PLEASE ENTER A VALID PROGRAM NAME.\n")

        Pro_Membership = Pro_Membership_fee()
        total_pro_discount, membership_fee = Pro_Membership.check_membership_fee()

        # Calculate Subtotal
        subtotal = sum(program['total_price'] for program in programs) + membership_fee
        print(f"\nSUB_TOTAL: ₹{subtotal:.2f}")

        # Apply B4G1 if applicable
        if Geekdemy.total_program_count >= 4:
            b4g1 = B4G1()
            coupon_discount, coupon_name = b4g1.cupons(subtotal, Geekdemy.total_program_count)
        else:
            # Allow user to apply coupons
            coupon_discount, coupon_name = Geekdemy.apply_coupons(subtotal, Geekdemy.total_program_count)

        # Subtotal after coupon
        subtotal_after_coupon = subtotal - coupon_discount

        # Apply Enrollment Fee
        enrollment_fee = EnrollmentFee.apply_enrollment_fee(subtotal_after_coupon)
        total_cost = subtotal_after_coupon + enrollment_fee

        # Print Bill Summary
        Geekdemy.print_bill_summary(subtotal, coupon_name, coupon_discount, total_pro_discount, membership_fee, enrollment_fee, total_cost)


    @staticmethod
    def apply_coupons(total_cost, total_count):
        available_coupons = {'deal_g20', 'deal_g5'}
        selected_coupons = set()

        print("\nAVAILABLE COUPONS: DEAL_G20, DEAL_G5")
        coupon = input("\nENTER COUPON TO APPLY (or 'done' to exit):\t").strip().lower()
        
        if coupon in available_coupons:
            selected_coupons.add(coupon)
        elif coupon != 'done':
            print("\nINVALID COUPON. PLEASE ENTER A VALID COUPON NAME.\n")

        if not selected_coupons or coupon == 'done':
            print("\nNO VALID COUPONS APPLIED.")
            return (0, 'DISCOUNT_NONE')

        # Calculate discounts for each selected coupon
        coupon_discounts = {}
        for coupon in selected_coupons:
            if coupon == 'deal_g20':
                deal_g20 = Deal_G20()
                discount, name = deal_g20.cupons(total_cost, total_count)
                if discount > 0:
                    coupon_discounts[name] = discount
            elif coupon == 'deal_g5':
                deal_g5 = Deal_G5()
                discount, name = deal_g5.cupons(total_cost, total_count)
                if discount > 0:
                    coupon_discounts[name] = discount

        if not coupon_discounts:
            print("\nNO VALID COUPONS APPLIED.")
            return (0, 'DISCOUNT_NONE')

        # Select the coupon with the highest discount
        best_coupon = max(coupon_discounts.items(), key=lambda x: x[1])
        # best_coupon is a tuple like ('DEAL_G20', 2000.0)
        return (best_coupon[1], best_coupon[0])  # (discount, coupon_name)


    @staticmethod
    def print_bill_summary(subtotal, coupon_name, coupon_discount, total_pro_discount, membership_fee, enrollment_fee, total_cost):
        print("\n===== BILL SUMMARY =====")
        print(f"SUB_TOTAL: ₹{subtotal:.2f}")
        print(f"COUPON_DISCOUNT {coupon_name}: ₹{coupon_discount:.2f}")
        print(f"TOTAL_PRO_DISCOUNT: ₹{total_pro_discount:.2f}")
        print(f"PRO_MEMBERSHIP_FEE: ₹{membership_fee:.2f}")
        print(f"ENROLLMENT_FEE: ₹{enrollment_fee:.2f}")
        print(f"TOTAL: ₹{total_cost:.2f}")
        print("========================\n")
        Geekdemy.exit_geekdemy()

    @staticmethod
    def exit_geekdemy():
        while True:
            ask = input("\nDO YOU WANT TO EXIT? (y/n):\t").strip().lower()
            if ask == 'y':
                print("\nTHANK YOU FOR USING GEEKDEMY!\n")
                input()
                exit(0)
            elif ask == 'n':
                print("\nRESTARTING GEEKDEMY...\n")
                # Reset global variables
                global programs
                programs.clear()
                # Reset class variables
                Geekdemy.total_program_count = 0
                Geekdemy.geekdemy()
            else:
                print("\nINVALID INPUT. PLEASE ENTER 'y' or 'n'.\n")
                Geekdemy.exit_geekdemy()


if __name__ == '__main__':
    Geekdemy.geekdemy()
