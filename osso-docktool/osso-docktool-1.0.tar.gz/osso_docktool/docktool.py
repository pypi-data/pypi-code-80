from __future__ import print_function

from datetime import datetime
from warnings import warn
import argparse
import os
import traceback
import stat
import sys

from . import settings
from .diskemptysampler import DiskEmptySampler
from .hdddock import BaseStorageDevice
from .inventoryrestclient import InventoryRESTClient
from .labelprinterapiclient import get_labelprinter


try:
    raw_input  # py2
except NameError:
    def raw_input(msg=None):  # py3
        if msg is not None:
            print(msg, end='')
        return input()


class SymlinkNotFound(Exception):
    pass


class DeviceManager(object):
    def __init__(self, hdd_dock, hdd_id, inventory_rest_client,
                 author, location):
        self._hdd_dock = hdd_dock
        self._hdd_id = hdd_id
        self._inventory_rest_client = inventory_rest_client
        self._author = author
        self._location = location

    def show_summary(self, print_data):
        do_print(print_data, self._hdd_dock)

    def show_commands(self):
        erase_methods = self._hdd_dock.get_erase_methods()
        next_erase_method = 0

        print('')
        print('Inventory-url: {}'.format(
            self._inventory_rest_client.get_hdd_url(self._hdd_id)))
        print('')
        print('Possible actions:')
        print('1. Change owner')
        print('2. Reprint label')
        print('3. Quick erase')
        if len(erase_methods) > 1:
            print('4. Secure erase ({})'.format(
                erase_methods[next_erase_method].name))
            next_erase_method += 1
        print('5. Change server bay')
        print('6. Change health status')
        print('7. Print health label')
        print('8. Secure erase ({})'.format(
            erase_methods[next_erase_method].name))
        print('D. Dispose HDD in security container')
        print('P. Show current info/status (again)')

        print('')
        print('9. Quit + EJECT (^C to skip eject)')

    def _set_status(self, status, extra_info):
        self._inventory_rest_client.add_status(
            self._hdd_id, status=status, extra_info=extra_info)

    def best_erase(self):
        erase_method = self._hdd_dock.get_erase_methods()[0]
        self._erase(erase_method)

    def second_best_erase(self):
        erase_methods = self._hdd_dock.get_erase_methods()
        if len(erase_methods) > 1:
            erase_methods.pop(0)
        self._erase(erase_methods[0])

    def _erase(self, erase_method):
        if erase_method.type == 'builtin':
            return self._erase_with_status(erase_method)
        if erase_method.type == 'manual':
            print('Secure disk wipe chosen. Please wait as this will '
                  'take a long time... - 1 pass lessrandom and 1 pass '
                  'zerofill\n')
            return self._erase_with_status(erase_method)
        raise NotImplementedError(erase_method)

    def _erase_with_status(self, erase_method):
        # Fetch vars.
        # XXX: better dynamic value for sample count based on disk size?
        sample_count = settings.POST_WIPE_SAMPLE_COUNT
        if self._hdd_dock.is_ssd():
            sample_count *= 20  # SSDs/NVMes are fast(er)
        sample_size = settings.POST_WIPE_SAMPLE_SIZE

        print('Attempting erase method {!r} on BLKDEV {!r}'.format(
            erase_method.name, self._hdd_dock.devname))

        # Running pre-sample! This is not needed, but nice during dev.
        if self._find_non_zero_blocks(sample_count, sample_size):
            print('DEBUG: Found non-zero samples before wipe (expected)')
        else:
            print('DEBUG: No non-zero sample found. Disk already zeroed?')

        print('Start secure wiping BLKDEV')
        success, error = erase_method()
        if not success:
            print('Error: {}'.format(error))
            self._set_status(
                'BLKDEV_SECURE_WIPED_ERROR', (
                    'Block device secure wipe error at {}: {} --{}'
                    .format(self._location, error, self._author)))
            return

        print('Block device securely wiped')

        # Running post-sample. Should be all zero.
        if self._find_non_zero_blocks(sample_count, sample_size):
            print('ERROR: Found non-empty sample!')
            print('Please check {!r} manually!'.format(self._hdd_dock.devname))
            self._set_status(
                'BLKDEV_SECURE_WIPED_ERROR', (
                    'Block device secure wipe {!r} error at {}, non-empty '
                    'samples found --{}'
                    .format(erase_method.name, self._location, self._author)))
            return

        print('OK: All samples are empty')
        self._set_status(
            'BLKDEV_SECURE_WIPED', (
                'Block device secure wiped using {!r} at {} and '
                'checked {} {} --{}'
                .format(
                    erase_method.name, self._location, sample_count,
                    sample_size, self._author)))

    def _find_non_zero_blocks(self, sample_count, sample_size):
        print(
            'DEBUG: Sampling block device to check if empty... '
            '(sample_count: {}, sample_size {})'.format(
                sample_count, sample_size))

        disk_empty_sampler = DiskEmptySampler(
            self._hdd_dock.devname, sample_count, sample_size)
        result = disk_empty_sampler.sample_disk()
        assert result is not None

        return result is False  # false = we found non-zero


def register_disk(**kwargs):
    # Python2-compatible forced kwargs. Temporary fix until we clean up this
    # code.
    hdd_dock = kwargs.pop('hdd_dock')
    inventory_rest_client = kwargs.pop('inventory_rest_client')
    author = kwargs.pop('author')
    location = kwargs.pop('location')
    assert not kwargs, None

    print('')
    print('Disk is not registered yet, please specify the following fields:')
    owner = raw_input('Owner [OSSO]: ')

    # Default to OSSO
    if owner in (None, ''):
        owner = 'OSSO'

    bay = raw_input('bay ['']: ')

    if bay in (None, ''):
        bay = ''

    erase = None
    while erase not in ('y', 'n', 'Y', 'N', ''):
        erase = raw_input('Quick erase? (y/N): ')

    result = inventory_rest_client.add_hdd(hdd_dock, bay)
    tag_uid = result['tag_uid']
    hdd_id = result['id']

    inventory_rest_client.add_smart_data(
        hdd_id, rawdata=hdd_dock.hwdata.rawdata)
    inventory_rest_client.add_status(
        hdd_id, status='REGISTERED',
        extra_info='Registered at {} --{}'.format(location, author))
    inventory_rest_client.add_owner(  # XXX: author-of-owner, not owner-eml
        hdd_id, name=owner, email=author)
    inventory_rest_client.add_location(
        hdd_id, location=location)

    if erase == 'y' or erase == 'Y':
        print('Start wiping')
        hdd_dock.quick_erase()
        inventory_rest_client.add_status(
            hdd_id, status='QUICK_WIPED',
            extra_info='Quick wiped at {} --{}'.format(location, author))
        print('Disk wiped')

    # Print label, unless the disk is in a remote machine
    if location != 'remote':
        labelprinter_rest_client = get_labelprinter()
        labelprinter_rest_client.print_hdd_label(
            tag_uid, hdd_dock.get_serial_number(), owner)

    raw_input('Registration complete, press enter')


def registered_disk_actions(**kwargs):
    # Python2-compatible forced kwargs. Temporary fix until we clean up this
    # code.
    hdd_dock = kwargs.pop('hdd_dock')
    hdd_id = kwargs.pop('hdd_id')
    inventory_rest_client = kwargs.pop('inventory_rest_client')
    static_data = kwargs.pop('static_data')
    dynamic_data = kwargs.pop('dynamic_data')
    author = kwargs.pop('author')
    location = kwargs.pop('location')
    assert not kwargs, None

    if not settings.DEBUG:
        # Always add smart data, even when disk is registered
        inventory_rest_client.add_smart_data(
            hdd_id, rawdata=hdd_dock.hwdata.rawdata)
        # Always add a status & location
        # of the disk being seen at OSSO HQ
        if location != 'remote':
            inventory_rest_client.add_status(
                hdd_id, status='CHECKED_IN',
                extra_info='Checked in at {} --{}'.format(location, author))
            inventory_rest_client.add_location(
                hdd_id, location=location)

    hdd = inventory_rest_client.get_hdd(hdd_id)[0]
    current_owner = hdd.get('current_owner', None)

    if current_owner:
        current_owner = current_owner.get('name', None)
    if not current_owner:
        current_owner = 'Notset'

    # current_status = hdd.get('status', None)

    # if current_status:
    #     current_status = current_status.get('name', None)
    # if not current_status:
    #     current_status = 'Notset'

    current_health_status = hdd.get('current_health', None)

    if current_health_status:
        current_health_status = current_health_status.get('status', None)

    if not current_health_status:
        current_health_status = 'Notset'

    print_data = static_data + dynamic_data

    print_data.append(['', '-'])
    print_data.append(['REGISTRATION INFORMATION', '-'])
    print_data.append(['=', '-'])
    print_data.append(['Disk is already registered as', hdd['id']])
    print_data.append(['Last owner', current_owner])
    # print_data.append(['Last status', current_status])
    print_data.append(['Last health status', current_health_status])
    print_data.append(['Server bay', hdd['bay'] or '-'])

    manager = DeviceManager(
        hdd_dock, hdd_id, inventory_rest_client, author, location)
    manager.show_summary(print_data)  # XXX: should not pass print_data here
    manager.show_commands()

    while True:
        action = raw_input('\nAction: ').upper()

        if action == '1':
            owner = ''
            while len(owner) == 0:
                owner = raw_input('New owner: ')
            inventory_rest_client.add_owner(  # XXX: not email-of-owner
                hdd_id, name=owner, email=author)
            current_owner = owner

        elif action == '2':
            # Print label
            labelprinter_rest_client = get_labelprinter()
            labelprinter_rest_client.print_hdd_label(
                hdd['tag_uid'],
                hdd_dock.get_serial_number(),
                current_owner)

        elif action == '3':
            print('Start quick wiping')
            hdd_dock.quick_erase()
            inventory_rest_client.add_status(
                hdd_id, status='QUICK_WIPED',
                extra_info='Quick wiped at {} --{}'.format(location, author))

            print('Disk/ssd quick wiped')

        elif action == '4':
            manager.best_erase()

        elif action == '5':
            bay = ''
            while len(bay) == 0:
                bay = raw_input('New server bay: ')
            hdd = inventory_rest_client.change_bay(
                hdd_id,
                bay)
            print('Server bay changed to: {}'.format(hdd['bay']))

        elif action == '6':
            health_status = ''
            while len(health_status) == 0:
                health_status = raw_input('New health status: ')
            inventory_rest_client.add_health_status(
                hdd_id, status=health_status, extra_info='--{}'.format(author))
            current_health_status = health_status

        elif action == '7':
            # Print label
            lines = [
                'Health status: {} @ {}'.format(
                    current_health_status.upper(),
                    datetime.now().strftime('%Y-%m-%d')),
                '',
                'Serial: {}'.format(hdd_dock.get_serial_number()),
            ]
            total_bytes_written = [
                x for x in dynamic_data
                if 'Total bytes written' in x[0]][0]
            total_bytes_read = [
                x for x in dynamic_data
                if 'Total bytes read' in x[0]][0]

            lines.append('Total bytes written/read: {}/{}'.format(
                total_bytes_written[1], total_bytes_read[1]))

            for item in ['Power on hours', 'Reallocated sector count']:
                lines += [
                    ' : '.join([x[0].rstrip(), x[1]])
                    for x in dynamic_data if item in x[0]]

            labelprinter_rest_client = get_labelprinter()
            labelprinter_rest_client.print_generic_label(lines)

        elif action == '8':
            manager.second_best_erase()

        elif action == '9':
            break  # Quit + EJECT

        elif action == 'D':
            assert location != 'remote', 'Cannot remote-dispose..'
            inventory_rest_client.add_status(
                hdd_id, status='HDD_DISPOSED',
                extra_info='Disposed in security container at {} --{}'.format(
                    location, author))
            inventory_rest_client.add_location(
                hdd_id, location='OSSO HQ: HDD security container')
            break

        elif action == 'P':
            # FIXME: print_data is stale!
            manager.show_summary(print_data)
            manager.show_commands()

        else:
            print('Notice: {!r} action unknown'.format(action))

    hdd_dock.shutdown_disk()
    exit(0)


def human_readable_bytes(byte_count):
    options = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']

    counter = 0
    while byte_count // 1024 > 0:
        byte_count = byte_count / 1024.0
        counter += 1
        if counter == len(options) - 1:
            break

    return '{} {}'.format(round(byte_count, 2), options[counter])


def do_print(data, hdd_dock):
    key_length = 0
    item_length = 0

    for key, item in data:
        key_length = max(key_length, len(key))
        item_length = max(item_length, len(item))

    print('DISK INFORMATION [BAY NR: {}]'.format(
        hdd_dock.docktool_bay_nr))

    print('=' * (key_length + item_length + 3))

    for x in data:
        if x[0] == '=':
            print('=' * (key_length + item_length + 3))
        elif x[1] == '-':
            print(x[0])
        else:
            x[0] = x[0] + ' ' * (key_length - len(x[0]))
            print(' : '.join(x))


def main_menu(devname):
    author = os.environ.get('EMAIL', '')
    if '@' not in author:
        print('ERROR: Please set the EMAIL envvar to specify who you are!')
        exit(1)
    location = os.environ.get('LOCATION', 'remote')
    if not location:
        print('ERROR: Please (un)set the LOCATION envvar to specify where!')
        exit(1)

    hdd_dock = BaseStorageDevice.from_devname(devname)
    hwdata = hdd_dock.hwdata
    sys.stdout.write('\x1b]2;DOCKTOOL DISK BAY: {}\x07'.format(
        hdd_dock.docktool_bay_nr))

    static_data = []

    static_data.append(['Device model', hdd_dock.get_device_model()])
    static_data.append(['Serial', hdd_dock.get_serial_number()])
    static_data.append(
        ['Device (port)', '{} ({})'.format(
            devname, hdd_dock.port if hdd_dock.port else 'Unknown')])
    static_data.append(['SSD', ('yes' if hdd_dock.is_ssd() else 'no')])
    static_data.append(
        ['SAS (detected)', ('yes' if hdd_dock.is_sas() else 'no')])
    static_data.append(['User Capacity', hdd_dock.get_user_capacity()])

    dynamic_data = []

    total_bytes_written = 'Notset'
    total_bytes_read = 'Notset'
    if hwdata.sector_size is not None:
        if hwdata.lbas_written is not None:
            total_bytes_written = human_readable_bytes(
                hwdata.sector_size * hwdata.lbas_written)
        if hwdata.lbas_read is not None:
            total_bytes_read = human_readable_bytes(
                hwdata.sector_size * hwdata.lbas_read)
    dynamic_data.append(['Total bytes written', total_bytes_written])
    dynamic_data.append(['Total bytes read', total_bytes_read])

    def _NS(value):
        if value is None:
            return 'Notset'
        return str(value)

    dynamic_data.append([
        'Power on hours',
        '{} hours'.format(_NS(hwdata.power_on_hours))])
    dynamic_data.append([
        'Wear leveling count',
        _NS(hwdata.wear_leveling_count)])
    dynamic_data.append([
        'Reallocated sector count',
        _NS(hwdata.reallocated_sector_ct)])
    dynamic_data.append([
        'Reallocated event count',
        _NS(hwdata.reallocated_event_count)])
    dynamic_data.append([
        'Current pending sector',
        _NS(hwdata.current_pending_sector)])
    dynamic_data.append([
        'Offline uncorrectable',
        _NS(hwdata.offline_uncorrectable)])

    inventory_rest_client = InventoryRESTClient(
        settings.DASHBOARD_BASE_URL)

    # HDD is an asset so asset_id = hdd_id
    try:
        hdd_id = inventory_rest_client.get_hdd_id(
            hdd_dock.get_device_model(),
            hdd_dock.get_serial_number())
    except ValueError as e:
        warn(str(e))
        do_print(static_data + dynamic_data, hdd_dock)
        raise

    print(
        '\n\x1b[1mBEWARE:\x1b[0m All your actions will be recorded '
        'as performed by: \x1b[1;32m{}\x1b[0m\n'
        'Change EMAIL envvar if it is incorrect!'.format(author))
    print(
        '\x1b[1mBEWARE:\x1b[0m LOCATION is set to: \x1b[1;32m{}\x1b[0m\n'
        'Change to "OSSO HQ: HDD docktool" if in the office.\n'
        .format(location))

    if hdd_id is None:
        do_print(static_data + dynamic_data, hdd_dock)
        register_disk(
            hdd_dock=hdd_dock,
            inventory_rest_client=inventory_rest_client,
            author=author, location=location)
        hdd_id = inventory_rest_client.get_hdd_id(
            hdd_dock.get_device_model(),
            hdd_dock.get_serial_number())
        assert hdd_id, 'HDD id not set after registration?'
    else:
        registered_disk_actions(
            hdd_dock=hdd_dock, hdd_id=hdd_id,
            inventory_rest_client=inventory_rest_client,
            static_data=static_data, dynamic_data=dynamic_data,
            author=author, location=location)


class DocktoolArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(
            description='Docktool for processing disks')  # exit_on_error=False
        self.add_argument(
            'device', metavar='DISK', type=self.block_device,
            help='Device to use for example: /dev/sda')
        self.message2 = None

    def exit(self, status=0, message=None):
        if self.message2:
            print('{prog}: {message}'.format(
                prog=self.prog, message=self.message2),
                file=sys.stderr)
            self.message2 = None
        elif len(sys.argv) == 1:
            try:
                candidates = sorted(set([
                    os.path.realpath(os.path.join('/dev/disk/by-id', i))
                    for i in os.listdir('/dev/disk/by-id')]))
            except FileNotFoundError:
                # ??? no /dev/disk/by-id?
                candidates = ['(no disks found?)']
            message2 = 'suggesting disks:{}'.format(
                '\n  '.join([''] + candidates))
            print('{prog}: {message}'.format(
                prog=self.prog, message=message2),
                file=sys.stderr)

        super().exit(status=0, message=message)

    def block_device(self, name):
        try:
            st = os.stat(name)
        except FileNotFoundError:
            if '/' not in name:
                ret = self.block_device('/dev/{}'.format(name))
                warn('Prepended /dev/ to the block device name')
                return ret
            self.message2 = '{!r}: not found'.format(name)
            raise argparse.ArgumentError('{}: not found'.format(name))
        if not stat.S_ISBLK(st.st_mode):
            self.message2 = '{!r}: not a block device'.format(name)
            raise argparse.ArgumentError('{}: not a block device'.format(name))
        if os.getuid() != 0:
            warn('Expected UID 0 (root) for access')
        return name


def main():
    parser = DocktoolArgumentParser()
    args = parser.parse_args()

    try:
        main_menu(args.device)
    except Exception as e:
        print('ERROR: {}\n'.format(e), file=sys.stderr)
        print()
        print(traceback.format_exc(), file=sys.stderr)
        raw_input('Error found, please inform developer. Press enter')
        raise e


if __name__ == '__main__':
    main()
