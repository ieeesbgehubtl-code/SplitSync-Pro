from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def q(value):
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def split_equal(total, user_ids):
    total = q(total)
    n = len(user_ids)
    if n <= 0:
        raise ValueError("At least one participant is required.")
    base = q(total / n)
    amounts = [base for _ in user_ids]
    amounts[-1] = q(total - sum(amounts[:-1]))
    return dict(zip(user_ids, amounts))


def split_exact(total, allocations):
    total = q(total)
    result = {k: q(v) for k, v in allocations.items()}
    if sum(result.values(), Decimal("0.00")) != total:
        raise ValueError("Participant amounts must equal expense amount.")
    return result


def split_percentage(total, percentages):
    if sum(Decimal(str(v)) for v in percentages.values()) != Decimal("100"):
        raise ValueError("Percentages must total 100.")
    total = q(total)
    keys = list(percentages)
    vals = [q(total * Decimal(str(percentages[k])) / Decimal("100")) for k in keys]
    vals[-1] = q(total - sum(vals[:-1]))
    return dict(zip(keys, vals))


def split_shares(total, shares):
    total_units = sum(Decimal(str(v)) for v in shares.values())
    if total_units <= 0:
        raise ValueError("Share units must be positive.")
    total = q(total)
    keys = list(shares)
    vals = [q(total * Decimal(str(shares[k])) / total_units) for k in keys]
    vals[-1] = q(total - sum(vals[:-1]))
    return dict(zip(keys, vals))


def simplify_balances(balances):
    debtors = sorted(
        [(u, q(-b)) for u, b in balances.items() if q(b) < 0],
        key=lambda x: x[1],
        reverse=True,
    )
    creditors = sorted(
        [(u, q(b)) for u, b in balances.items() if q(b) > 0],
        key=lambda x: x[1],
        reverse=True,
    )
    settlements = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        d, owed = debtors[i]
        c, due = creditors[j]
        amount = min(owed, due)
        if amount > 0:
            settlements.append({"from_user": d, "to_user": c, "amount": q(amount)})
        owed = q(owed - amount)
        due = q(due - amount)
        debtors[i] = (d, owed)
        creditors[j] = (c, due)
        if owed == 0:
            i += 1
        if due == 0:
            j += 1
    return settlements
