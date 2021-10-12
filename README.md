<p align="center">
  <img alt="Orthrus Logo" src="agent_icons/orthrus.svg" height="30%" width="30%">
</p>

# Orthrus

Orthrus is a macOS agent that uses Apple's MDM to backdoor a device using a malicious profile. It effectively runs its own MDM server and allows the operator to interface with it using Mythic.

## Talks & Publications

- Orthrus was presented in the Black Hat USA 2021 talk [Come to the Dark Side, We Have Apples: Turning macOS Management Evil](https://www.blackhat.com/us-21/briefings/schedule/index.html#come-to-the-dark-side-we-have-apples-turning-macos-management-evil-23582).

- Further information about detecting Orthrus can be found at [TheMacPack.io - Detecting Orthrus and Typhon](https://themacpack.io/posts/Detecting-Orthrus-and-Typhon/)

## Installation
To install Orthrus, you'll need Mythic installed on a remote computer. You can find installation instructions for Mythic at the [Mythic project page](https://github.com/its-a-feature/Mythic/).

From the Mythic install root, run the command:

`./mythic-cli install github https://github.com/MythicAgents/orthrus.git`

Once installed, restart Mythic.

Orthrus uses Apple's Push Notification Service to send messages to the target device. For this reason, we need to configure APN push certificates. Some of the options for this can be found at [Understanding MDM Certificates](https://micromdm.io/blog/certificates/). 

In my opinion, installing Server.app, setting up Profile Manager and then exporting the push cert from the keychain is the easiest way to do this. Full instructions for getting the APN certs in a more permanent way can be found [here](https://github.com/micromdm/micromdm/blob/master/docs/user-guide/quickstart.md#configure-an-apns-certificate).

Instead of running the `mdmctl mdmcert upload` command manually, put the certificates in the `C2_Profiles/mdm/certs/` folder, as `apn.pem` and `apn.key`. 

Next, generate a SSL certificate for your MDM server.

```
DNSNAME=mdm.example.org;  (cat /etc/ssl/openssl.cnf ; printf "\n[SAN]\nsubjectAltName=DNS:$DNSNAME\n") | openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -sha256 -keyout mdm.key -out mdm.crt -subj "/CN=$DNSNAME" -reqexts SAN -extensions SAN -config /dev/stdin
```

Once created, base64 both the key and the certificate and put them in the config file using the Mythic UI for the MDM C2 Profile (Global Configurations -> C2 Profiles -> MDM -> Configure). Also set the `mdm_host` config item whilst you're here. 

Restart the container.

```
./mythic-cli c2 start mdm
```

and you're good to go.

## Notable Features
- No custom code introduced to the device.
- No beaconing behaviour, Orthrus will check in to Mythic when the operator tells it to using the `force_callback` command.
- SSL certificate of the MDM server trusted for code signing upon installation.
- Install PKG installers or Profiles.

## Executing Packages

### Signing

`mdmclient` will only execute packages that have been signed. If you do not use a signed package, it will silently fail. Usefully, the compromised device will install the TLS certificate of the MDM server (specified in the config) as a CA trusted for code sigining.

First, on an attacker box. Build a PFX file using the certificate and key from the MDM server.

```
openssl pkcs12 -export -out mdm.pfx -inkey mdm.key -in mdm.crt
```

Open the resulting pfx file to install it into the keychain.

The certificate can now be used as a signing identity. 


### pkg-cmd-helper

To automate the process of creating a signed package. I've put together a rough bash script to build packages that execute bash command, and subsequently sign them with an identity - [pkg-cmd-helper.sh](https://gist.github.com/rookuu/49ea14a50854542ca7f5cde70962e502).

```
➜  ./pkg-cmd-helper.sh -h
Command line helper to generate pkg files that execute commands.
Author: @rookuu

Syntax: gen.sh -i com.malicious.pkg -o installme.pkg [-s 'My Signing Identity'] command
options:
-h     Print this Help.
-i     Identifier for the package.
-o     File name for the output package.
-s     (optional) Identity to use when signing the package.

➜  ./pkg-cmd-helper.sh -i com.rookuu.pkg -o example.pkg -s 192.168.0.5 mkdir /tmp/hacked
Building in /var/folders/fc/lc78954d3mnfvn4wbz8_20nc0000gn/T/tmp.mmsY0R6i
pkgbuild: Adding top-level preinstall script
pkgbuild: Wrote package to /var/folders/fc/lc78954d3mnfvn4wbz8_20nc0000gn/T/tmp.mmsY0R6i/temp.pkg
productbuild: Wrote product to /var/folders/fc/lc78954d3mnfvn4wbz8_20nc0000gn/T/tmp.mmsY0R6i/temp_dist.pkg
productsign: signing product with identity "192.168.0.5" from keychain /Library/Keychains/System.keychain
productsign: Wrote signed product archive to /var/folders/fc/lc78954d3mnfvn4wbz8_20nc0000gn/T/tmp.mmsY0R6i/temp_dist_signed.pkg
Done, see: example.pkg
```

## Commands Manual Quick Reference

The commands available to us are dependent on the Apple MDM protocol, a full list of commands can be found on Apple's developer docs [here](https://developer.apple.com/documentation/devicemanagement/commands_and_queries).

### General Commands

Command | Syntax | Description
------- | ------ | -----------
force\_callback | `force_callback` | Sends a push notification to the device, forcing it to checkin.
certificate\_list | `certificate_list` | Lists installed certificates.
device\_information | `device_information` | Returns general information about the device.
installed\_applications | `installed_applications` | Lists installed applications.
profile\_list | `profile_list` | Lists installed profiles.
provisioning\_profile\_list | `provisioning_profile_list` | Lists installed provisioning profiles.
security\_info | `security_info` | Returns information about the security settings and features for the device.
install\_profile | `install_profile` | Installs a mobile config file (upload using UI).
install\_pkg | `install_pkg` | Installs a PKG installer file (upload using UI). Must be signed, see above.


## Thanks

- [@its_a_feature_](https://twitter.com/its_a_feature_) for helping to troubleshoot all of the bugs in my code. :)
- [@1njection](https://twitter.com/1njection) for prior art on the topic, checkout the blog here (lots of other cool stuff here too) http://lockboxx.blogspot.com/2019/04/macos-red-teaming-203-mdm-mobile-device.html. 
