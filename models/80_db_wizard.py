#!/usr/bin/env python
# -*- coding: utf-8 -*-

from meshkit import *
import uci

if config is not None:
    db.define_table(
        'imageconf',
        Field(
            'id_user',
            db.auth_user,
            label=T('User ID'),
            comment=T('Id of the user who created this build.'),
            requires=IS_EMPTY_OR(
                IS_IN_DB(
                    db, db.auth_user.id, '%(username)s', zero=T('None'),
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('User ID'))
                )
            )
        ),
        Field(
            'target',
            label=T('Target'),
            comment=T(
                'For which hardware platform you want to build an image. If ' +
                'you are unsure which is the right one for your device ' +
                'vist the openwrt wiki and search for your device there.'
            ),
            requires=IS_IN_SET(
                available_targets,
                error_message=T(
                    '%(name)s is invalid'
                ) % dict(name=T('Target')),
                zero=None
            ),
        ),
        db.build_log.status,
        Field(
            'noconf',
            'boolean',
            label=T("No configuration"),
            comment=T(
                'If you check this option meshkit will only build your ' +
                'images, but not configure your system. Also it is still ' +
                'possible to select packages and upload your own files.'
            )
        ),
        db.user_defaults.expert,
        Field(
            'mail',
            label=T('Email'),
            comment=CAT(
                P(
                    T(
                        'Enter your email address here. After the images have '
                        'been built you will receive an email with download '
                        'links for the firmware.'
                    ),
                ),
                DIV(
                    T(
                        'This field is not mandatory, you can also use '
                        'Meshkit without entering your email address here.'
                    ),
                    _class="alert alert-info"
                )
            ),
            requires=IS_EMPTY_OR(
                IS_EMAIL(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Email'))
                )
            ),
        ),
        db.user_defaults.community,
        Field(
            'nodenumber',
            label=T('Nodenumber'),
            comment=T(
                'Please enter the Node Number for your weimarnetz node.'
            ),
            requires=IS_EMPTY_OR(
                IS_DECIMAL_IN_RANGE(
                    1, 1000,
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Node Number'))
                )
            )
        ),
        db.user_defaults.password_hash.clone(label=T('Password')),
        db.user_defaults.pubkeys,
        Field(
            'profile',
            label=T('Profile'),
            comment=T(
                'This sets a profile for your router model. If your device ' +
                'is not listed try something generic (default) if available.'
            ),
            requires=IS_EMPTY_OR(
                IS_MATCH(
                    '[a-zA-Z0-9\-]+',
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Profile'))
                )
            )
        ),
        Field(
            'webif',
            'list:reference gui',
            label=T('Web Interface'),
            comment=T(
                'Webinterface that is installed. ' +
                'This may remove or add packages depending on your selection.'
            ),
            requires=IS_IN_DB(
                db, db.gui.id, '%(full_name)s', zero=None,
            ),
            widget=select_webif_options
        ),
        Field(
            'theme',
            label=T('Theme'),
            comment=T(
                'Chooses the theme for the web interface. Freifunk-generic ' +
                'is the only one that is customised for communities, so you ' +
                'should probably use this theme.'
            ),
            requires=IS_EMPTY_OR(
                IS_IN_SET(
                    themes,
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Theme'))
                )
            )
        ),
        Field(
            'ipv6',
            'boolean',
            label=T('IPv6'),
            default=False,
            comment=T('Enable/Disable IPv6 globally.')
        ),
        Field(
            'ipv6_config',
            requires=IS_EMPTY_OR(
                IS_IN_SET(
                    ['static', 'auto-ipv6-random', 'auto-ipv6-fromv4'],
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Webinterface'))
                )
            )
        ),
        Field(
            'packages',
            type='text',
            label=T('Packages'),
            requires=IS_EMPTY_OR(
                IS_MATCH(
                    '[a-zA-Z0-9\-\_\n]+',
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Packages'))
                )
            )
        ),
        Field(
            'rand',
            requires=IS_EMPTY_OR(
                [
                    IS_ALPHANUMERIC(),
                    IS_LENGTH(32)
                ]
            )
        ),
        Field(
            'hostname',
            requires=IS_EMPTY_OR(
                IS_MATCH(
                    '^[a-zA-Z0-9][a-zA-Z0-9\.\-]+[a-zA-Z0-9]$',
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Hostname'))
                )
            ),
            comment=T(
                'Hostname. If left empty it will be autogenerated ' +
                'from the IPv4 address'
            )
        ),
        db.user_defaults.latitude,
        db.user_defaults.longitude,
        Field(
            'upload',
            'upload',
            requires=IS_EMPTY_OR(
                IS_UPLOAD_FILENAME(
                    extension='gz',
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Upload'))
                )
            )
        ),
        Field('wifiifsnr', 'integer'),
        db.user_defaults.nickname,
        db.user_defaults.name,
        db.user_defaults.email,
        db.user_defaults.phone,
        db.user_defaults.location,
        db.user_defaults.homepage,
        db.user_defaults.note,
        Field(
            'wanproto',
            label=T('WAN Protocol'),
            comment=T('Protocol to use for the WAN interface.'),
            requires=IS_EMPTY_OR(
                IS_IN_SET(
                    config.wanprotos,
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Wan Protocol'))
                )
            )
        ),
        Field(
            'wanipv4addr',
            label=T('IPv4 Address'),
            length=15,
            comment=T('IPv4 address for the wan interface'),
            requires=IS_EMPTY_OR(
                IS_IPV4(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='WAN ' + T('IP address'))
                )
            )
        ),
        Field(
            'wannetmask',
            label=T('Netmask'),
            length=15,
            comment=T('IPv4 netmask for the wan interface'),
            requires=IS_EMPTY_OR(
                IS_IPV4(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='WAN ' + T('Netmask'))
                )
            )
        ),
        Field(
            'wangateway',
            label=T('Gateway'),
            length=15,
            comment=T('Internet gateway'),
            requires=IS_EMPTY_OR(
                IS_IPV4(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='WAN ' + T('Gateway'))
                )
            )
        ),
        Field(
            'wandns',
            label=T('DNS'),
            length=255,
            comment=T(
                'DNS server(s). Seperate by space if you want to use ' +
                'multiple DNS servers.'
            ),
            requires=IS_EMPTY_OR(
                IS_MATCH(
                    '[0-9\. ]+',
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Profile'))
                )
            )
        ),
        Field(
            'wan_allow_ssh',
            'boolean',
            label=T('Allow ssh'),
            comment=T(
                'Add firewall rule to allow ssh access from the wan interface.'
            )
        ),
        Field(
            'wan_allow_web',
            'boolean',
            label=T('Allow web'),
            comment=T(
                'Add firewall rule to allow web access from the wan interface.'
            )
        ),
        Field(
            'sharenet',
            'boolean',
            label=T('Share internet'),
            comment=T(
                'Allow others in the mesh to use your internet connection. '
                'This makes use of the olsrd dyngw_plain plugin, which '
                'checks for available internet connectivity and starts to '
                'announce it as hna as soon as it is detected.'
            )
        ),
        Field(
            'localrestrict',
            'boolean',
            label=T('Protect local network'),
            default=True,
            comment=T(
                'Protect the network behind wan from being accessed from ' +
                'the mesh.'
            ),
        ),
        Field(
            'wan_qos',
            'boolean',
            label=T('QOS'),
            comment=T(
                'Adds traffic shaping with a fixed down- and upload limit ' +
                'to the WAN-Interface.'
            )
        ),
        Field(
            'wan_qos_down',
            'integer',
            label=T('Download speed'),
            default='1024',
            comment=T(
                'Download speed in kbit/s. Set it about 10% lower than your ' +
                'actual internet download speed.'
            ),
            widget=lambda k, v: input_nouislider(k, v, preset='bandwidth')
        ),
        Field(
            'wan_qos_up',
            'integer',
            label=T('Upload speed'),
            default='128',
            comment=T(
                'Upload speed in kbit/s. Set it about 10% lower than your ' +
                'actual internet upload speed.'
            ),
            widget=lambda k, v: input_nouislider(k, v, preset='bandwidth')
        ),
        Field(
            'lanproto',
            label=T('LAN Protocol'),
            comment=T('Protocol to use for the LAN interface.'),
            requires=IS_EMPTY_OR(
                IS_IN_SET(
                    config.lanprotos,
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='LAN ' + T('Protocol')),
                )
            )
        ),
        Field(
            'lanipv4addr',
            label=T('IPv4 Address'),
            length=15,
            default="192.168.1.1",
            comment=T('IPv4 address for the LAN interface'),
            requires=IS_EMPTY_OR(
                IS_IPV4(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='LAN ' + T('IP address'))
                )
            )
        ),
        Field(
            'lannetmask',
            label=T('Netmask'),
            length=15,
            default="255.255.255.0",
            comment=T('IPv4 netmask for the LAN interface'),
            requires=IS_EMPTY_OR(
                IS_IPV4(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='LAN ' + T('Netmask'))
                )
            )
        ),
        Field(
            'lanipv6addr',
            length=255,
            label=T('IPv6 Address'),
            comment=T('IPv6 address for the LAN interface'),
            requires=IS_EMPTY_OR(
                IS_IPV6CIDR(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='LAN ' + T('IPv6 address'))
                )
            )
        ),
        Field('lanipv6ra', 'boolean'),
        Field(
            'landhcp',
            'boolean',
            label=T('Enable DHCP'),
            comment=T('Enable DHCP-Server for the LAN interface.')
        ),
        Field(
            'landhcprange',
            requires=IS_EMPTY_OR(
                IS_IPV4CIDR(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name='LAN ' + T('DHCP Range'))
                )
            )
        ),
        Field(
            'url',
            requires=IS_EMPTY_OR(
                IS_URL(
                    mode='generic',
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('URL'))
                )
            )
        ),
        Field(
            'lang',
            length=8,
            requires=IS_EMPTY_OR(
                IS_MATCH('[a-zA-Z]+')
            )
        ),
    )

    db.define_table(
        'wifi_interfaces',
        Field(
            'ipv4addr',
            label=T('IPv4 Address'),
            length=15,
            default='1.2.3.4',
            comment=T('IPv4 address for this interface.'),
            requires=IS_EMPTY_OR(
                IS_IPV4(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('IP address'))
                )
            ),
        ),
        Field(
            'ipv6addr',
            label=T('IPv6 Address'),
            length=255,
            comment=T('IPv6 address for this interface.'),
            requires=IS_EMPTY_OR(
                IS_IPV6CIDR(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('IPv6 address'))
                )
            )
        ),
        Field(
            'ipv6ra',
            'boolean',
            label=T('Router Advertisement'),
            comment=T('Send IPv6 router advertisements.'),
            default=False
        ),
        Field(
            'chan',
            'integer',
            length=4,
            label=T('Channel'),
            comment=T('Channel to operate on.'),
            requires=IS_EMPTY_OR(
                IS_INT_IN_RANGE(
                    1, 170,
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('Channel'))
                )
            )
        ),
        Field(
            'dhcp',
            'boolean',
            label=T('Enable DHCP'),
            default=True,
            comment=T(
                'Enable DHCP and allow guests to connect to the network ' +
                'without using olsrd.'
            ),
        ),
        Field(
            'vap',
            'boolean',
            label=T('VAP'),
            default=True,
            comment=T(
                'Configure a VAP as Access Point. Only with drivers that ' +
                'support this. At the moment these are madwifi, ath5k and ' +
                'ath9k.'
            ),
        ),
        Field(
            'dhcprange',
            length=18,
            label=T('DHCP Range'),
            comment=T(
                'The range from which clients are assigned IP adresses. ' +
                'If it is inside your mesh network, then clients are ' +
                'announced as HNA by olsrd. If it is outside, they are ' +
                'natted. If left blank then a range is autocalculated ' +
                'from 6.0.0.0/8.'
            ),
            requires=IS_EMPTY_OR(
                IS_IPV4CIDR(
                    error_message=T(
                        '%(name)s is invalid'
                    ) % dict(name=T('DHCP Range'))
                )
            )
        ),
        Field(
            'enabled',
            'boolean',
            label=T("Enabled"),
            comment=T('If the interface is enabled.')
        ),
        Field(
            'id_build',
            db.imageconf,
            label=T("Build ID"),
            comment=T('The parent ID this interface belongs to.')
        ),
    )

if session.community:
    c = uci.UCI(config.profiles, "profile_" + session.community)
    community_defaults = cache.ram(
        'community_defaults_%s' % session.community,
        lambda: c.read(),
        time_expire=settings.cache_validity_time_long
    )
    defchannel = c.get(community_defaults, 'wifi_device', 'channel', '1')
    mesh_network = c.get(
        community_defaults,
        'profile',
        'mesh_network',
        '10.0.0.0/8'
    )
    defipv4 = defip(mesh_network)
    ipv6 = c.get(community_defaults, 'profile', 'ipv6', '0')
    ipv6_config = c.get(community_defaults, 'profile', 'ipv6_config', False)
    vap = c.get(community_defaults, 'profile', 'vap', '0')
    adhoc_dhcp_when_vap = c.get(
        community_defaults,
        'profile',
        'adhoc_dhcp_when_vap',
        '0'
    )

    session.community_packages = c.get(
        community_defaults,
        'profile',
        'extrapackages',
        ''
    )

    # db.wifi_interfaces defaults
    db.wifi_interfaces.chan.default = defchannel
    db.wifi_interfaces.ipv4addr.default = defipv4
    if vap == '1':
        db.wifi_interfaces.vap.default = True
    if adhoc_dhcp_when_vap == 1:
        db.wifi_interfaces.dhcp.default = True

    if ipv6 == '1':
        session.ipv6 = True
        session.ipv6conf = True
        session.ipv6_config = ipv6_config
        db.wifi_interfaces.ipv6ra.default = True
    else:
        session.ipv6 = False
        session.ipv6conf = False
        session.ipv6_config = None

    # db-imageconf defaults
    db.imageconf.theme.default = c.get(
        community_defaults,
        'profile',
        'theme',
        config.defaulttheme
    )
    if ipv6 == '1':
        db.imageconf.ipv6.default = True
