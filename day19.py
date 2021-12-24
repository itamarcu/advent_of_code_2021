import dataclasses
import itertools
from dataclasses import dataclass
from typing import Set, List, Dict

LARGE_AMOUNT = 12  # maybe 11


@dataclass
class Beacon:
    scanner_index: int
    index: int
    x: int
    y: int
    z: int
    neighbor_distances: Set[int]


Orientation = (str, str, str)  # e.g. 'x', 'y', 'z' or 'x', '-z', 'y'
ORIENTATIONS = []


def init_orientations():
    for perm in list(itertools.permutations(['x', 'y', 'z'])):
        for n in range(8):
            binary_representation = "{0:b}".format(n).zfill(3)
            pluses_and_minuses = ['+' if c == '1' else '-' for c in binary_representation]
            x, y, z = (pluses_and_minuses[k] + perm[k] for k in range(3))
            ORIENTATIONS.append((x, y, z))


@dataclass
class Scanner:
    index: int
    beacons: List[Beacon]
    orientation: Orientation = None
    world_coords: (int, int, int) = None


# actually this is distance to the power of 2, but we compare them so we ignore this
def calc_distance_between_coords(b1, b2):
    return (b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2 + (b1.z - b2.z) ** 2


def sign(c):
    return 1 if c == '+' else -1


def reorient_coord(scrambled_beacon: Beacon, orientation: Orientation, beacon_1: Beacon, beacon_2: Beacon):
    '''
    given a fixed (correct) beacon 1 at identity (x,y,z) orientation,
    and given beacon 2 which is (assumed to be) identical to beacon 1 under the orientation,
    we find out how much beacon 2 should have been moved to be where beacon 1 is,
    and then return the coords of scrambled_beacon based on this offset and this orientation
    '''
    o_x_sign, o_x_axis = orientation[0]  # e.g. ('+'. 'x') or e.g. ('-', 'z')
    o_y_sign, o_y_axis = orientation[1]
    o_z_sign, o_z_axis = orientation[2]
    # hacky but works
    b2_x = beacon_2.__dict__[o_x_axis] * sign(o_x_sign)
    b2_y = beacon_2.__dict__[o_y_axis] * sign(o_y_sign)
    b2_z = beacon_2.__dict__[o_z_axis] * sign(o_z_sign)
    sb_x = scrambled_beacon.__dict__[o_x_axis] * sign(o_x_sign)
    sb_y = scrambled_beacon.__dict__[o_y_axis] * sign(o_y_sign)
    sb_z = scrambled_beacon.__dict__[o_z_axis] * sign(o_z_sign)
    return (
        sb_x + beacon_1.x - b2_x,
        sb_y + beacon_1.y - b2_y,
        sb_z + beacon_1.z - b2_z,
    )


def calc_scanner_offset(orientation: Orientation, beacon_1: Beacon, beacon_2: Beacon):
    o_x_sign, o_x_axis = orientation[0]  # e.g. ('+'. 'x') or e.g. ('-', 'z')
    o_y_sign, o_y_axis = orientation[1]
    o_z_sign, o_z_axis = orientation[2]
    # hacky but works
    b2_x = beacon_2.__dict__[o_x_axis] * sign(o_x_sign)
    b2_y = beacon_2.__dict__[o_y_axis] * sign(o_y_sign)
    b2_z = beacon_2.__dict__[o_z_axis] * sign(o_z_sign)
    return (
        beacon_1.x - b2_x,
        beacon_1.y - b2_y,
        beacon_1.z - b2_z,
    )


def manhattan_distance(s1, s2):
    return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + abs(s1[2] - s2[2])


def main():
    init_orientations()
    with open('day19.txt') as input_file:
        input_lines = input_file.readlines()
    lines = [line.rstrip('\n') for line in input_lines]

    scanners = []
    scanner_num = -1
    beacon_num = -1
    curr_scanner_parse = []
    for line in lines:
        if line.startswith('---'):
            scanner_num += 1
            curr_scanner_parse = Scanner(index=scanner_num, beacons=[])
            beacon_num = -1
        elif line == '':
            scanners.append(curr_scanner_parse)
        else:
            x, y, z = [int(n) for n in line.split(',')]
            beacon_num += 1
            curr_scanner_parse.beacons.append(Beacon(
                index=beacon_num,
                scanner_index=scanner_num,
                x=x,
                y=y,
                z=z,
                neighbor_distances=set()
            ))
    scanners.append(curr_scanner_parse)

    scanners[0].orientation = ('+x', '+y', '+z')
    scanners[0].world_coords = (0, 0, 0)

    beacons_matching_specific_distances: Dict[int, List[Beacon]] = {}
    for scanner in scanners:
        for beacon in scanner.beacons:
            for other_beacon in scanner.beacons:
                beacon_distance = calc_distance_between_coords(beacon, other_beacon)
                beacon.neighbor_distances.add(beacon_distance)
                if beacon_distance == 0:
                    continue
                if beacon_distance not in beacons_matching_specific_distances:
                    beacons_matching_specific_distances[beacon_distance] = []
                beacons_matching_specific_distances[beacon_distance].append(beacon)
                beacons_matching_specific_distances[beacon_distance].append(other_beacon)

    suspects = []
    for distance in beacons_matching_specific_distances:
        beacons = beacons_matching_specific_distances[distance]
        for beacon_1 in beacons:
            for beacon_2 in beacons:
                # we know these two share one identical distance.  but do they share 12+ distances?
                # (and aren't from same scanner)
                if beacon_1.scanner_index == beacon_2.scanner_index:
                    continue
                # we will only try solving further if scanner 1's orientation is good and scanner 2's is bad

                intersections = beacon_1.neighbor_distances.intersection(beacon_2.neighbor_distances)
                if len(intersections) >= LARGE_AMOUNT:
                    # probably the same beacon from two different scanners!
                    suspects.append((beacon_1, beacon_2))

    while suspects:
        beacon_1, beacon_2 = suspects.pop(0)
        beacon_2 = dataclasses.replace(beacon_2)
        if scanners[beacon_1.scanner_index].orientation is None:
            # we will solve these later
            suspects.append((beacon_1, beacon_2))
            continue
        if scanners[beacon_2.scanner_index].orientation is not None:
            continue
        fixed_scanner = scanners[beacon_1.scanner_index]
        scrambled_scanner = scanners[beacon_2.scanner_index]
        existing_correct_beacon_coords = set((b.x, b.y, b.z) for b in fixed_scanner.beacons)
        for orientation in ORIENTATIONS:
            success_count = 0
            for scrambled_beacon_3 in scrambled_scanner.beacons:
                unscrambled_beacon_3_attempt = reorient_coord(scrambled_beacon_3, orientation, beacon_1, beacon_2)
                if unscrambled_beacon_3_attempt in existing_correct_beacon_coords:
                    success_count += 1
            if success_count >= LARGE_AMOUNT:
                # indeed, we found the right scanner pair and orientation!
                scrambled_scanner.orientation = orientation
                for b in scrambled_scanner.beacons:
                    x, y, z = reorient_coord(b, orientation, beacon_1, beacon_2)
                    b.x, b.y, b.z = (x, y, z)
                scrambled_scanner.world_coords = calc_scanner_offset(orientation, beacon_1, beacon_2)
                break

    # now all the scanners are correctly positioned and oriented!
    # and all the beacons!
    all_beacon_locations = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            all_beacon_locations.add((beacon.x, beacon.y, beacon.z))
    print(len(all_beacon_locations))  # 425

    biggest_distance = 0
    for scanner_1 in scanners:
        for scanner_2 in scanners:
            distance = manhattan_distance(scanner_1.world_coords, scanner_2.world_coords)
            biggest_distance = max(biggest_distance, distance)
    print(biggest_distance)  # 13354


if __name__ == '__main__':
    main()