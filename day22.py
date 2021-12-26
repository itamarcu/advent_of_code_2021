import re
import collections


def main():
    with open('day22.txt') as input_file:
        input_lines = input_file.readlines()
    lines = [line.rstrip('\n') for line in input_lines]
    solve(lines, True)  # 655005
    solve(lines, False)  # 1125649856443608


def solve(lines, limit_to_fifty: bool):
    # boxes turned "on" here will have a count of +1, boxes turned off have -1, intersections may add extras
    box_counts = collections.Counter()
    for line in lines:
        parsed = re.fullmatch(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', line)
        on_or_off, *coords = parsed.groups()
        if limit_to_fifty and max(abs(int(s)) for s in coords) > 50:
            continue
        # coordinates of this new box
        x0, x1, y0, y1, z0, z1 = [int(s) for s in coords]
        update = collections.Counter()
        if on_or_off == 'on':
            update[(x0, x1, y0, y1, z0, z1)] += 1
        for existing_box, existing_box_signed_count in box_counts.items():
            # coordinates of the existing box
            ex0, ex1, ey0, ey1, ez0, ez1 = existing_box
            # calculating coordinates of the intersection between them
            ix0 = max(x0, ex0)
            ix1 = min(x1, ex1)
            iy0 = max(y0, ey0)
            iy1 = min(y1, ey1)
            iz0 = max(z0, ez0)
            iz1 = min(z1, ez1)
            # if they didn't intersect, these conditions won't be true
            if ix0 <= ix1 and iy0 <= iy1 and iz0 <= iz1:
                # so if they do intersect we want to un-count the intersection
                update[(ix0, ix1, iy0, iy1, iz0, iz1)] -= existing_box_signed_count
        box_counts.update(update)
        # small speedup optimization here: delete every new thing in box_counts with a count of 0
        for key in update.keys():
            if box_counts[key] == 0:
                box_counts.pop(key)
    # summing up the boxes - note that some of them may have a negative count!
    print(sum((x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * signed_count
              for (x0, x1, y0, y1, z0, z1), signed_count in box_counts.items()))


if __name__ == '__main__':
    main()
