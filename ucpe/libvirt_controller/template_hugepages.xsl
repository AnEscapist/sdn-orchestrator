<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">
    <xsl:output omit-xml-declaration="yes" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <!--6-26-19: do not set the hugepages_memory variable here.  it will be overwritten. -->
    <xsl:variable name="hugepages_memory">HUGEPAGES_MEMORY</xsl:variable>
    <xsl:template match="/">
        <domain xmlns:qemu="http://libvirt.org/schemas/domain/qemu/1.0" type="kvm">
            <name>NAME</name>
            <memory unit="G">MEMORY</memory>
            <vcpu placement="static">VCPU_COUNT</vcpu>
            <!-- for cpu pinning
            <cputune>
            <vcpupin vcpu="0" cpuset="9"/>
            <vcpupin vcpu="1" cpuset="10"/>
            <vcpupin vcpu="2" cpuset="11"/>
            </cputune>
            -->
            <resource>
                <partition>/machine</partition>
            </resource>
            <os>
                <type arch="x86_64" machine="pc-i440fx-xenial">hvm</type>
                <boot dev="hd"/>
            </os>
            <features>
                <acpi/>
                <apic/>
                <pae/>
            </features>
            <cpu mode="host-model">
                <model fallback="allow"/>
                <feature policy='require' name='vmx'/>
            </cpu>
            <on_poweroff>destroy</on_poweroff>
            <on_reboot>restart</on_reboot>
            <on_crash>restart</on_crash>
            <clock offset="utc"/>
            <devices>
                <emulator>/usr/bin/kvm</emulator>
                <!-- for linux bridge interfaces
                <interface type="bridge">
                <source bridge="mgmtbr"/>
                <target dev="vnet5"/>
                <model type="virtio"/>
                <alias name="net0"/>
                <link state="up"/>
                </interface>
                -->
                <!-- for dpdk vhostuser interfaces
                <interface type="vhostuser">
                <source mode="client" path="/usr/local/var/run/openvswitch/vyatta_eth0" type="unix"/>
                <guest dev="eth3"/>
                <model type="virtio"/>
                <alias name="net1"/>
                <link state="up"/>
                </interface>
                -->
                <!--
                <interface type='hostdev' managed='yes'>
                  <source>
                    <address type='pci' domain='0' bus='11' slot='16' function='0'/>
                  </source>
                </interface>
                -->
                <disk device="disk" type="file">
                    <driver name="qemu" type="qcow2"/>
                    <source file="/var/third-party/BASE_IMAGE"/>
                    <backingStore/>
                    <target bus="virtio" dev="vda"/>
                    <alias name="virtio-disk0"/>
                </disk>
                <controller index="0" type="usb">
                    <alias name="usb"/>
                </controller>
                <controller index="0" model="pci-root" type="pci">
                    <alias name="pci.0"/>
                </controller>
                <serial type="pty">
                    <source path="/dev/pts/6"/>
                    <target port="0"/>
                    <alias name="serial0"/>
                </serial>
                <console tty="/dev/pts/6" type="pty">
                    <source path="/dev/pts/6"/>
                    <target port="0" type="serial"/>
                    <alias name="serial0"/>
                </console>
                <input tty="ps2" type="mouse"/>
                <input tty="ps2" type="keyboard"/>
                <graphics autoport="yes" listen="0.0.0.0" type="vnc"/>
                <video/>
                <memballoon model="none">
                    <alias name="balloon0"/>
                </memballoon>
            </devices>
            <qemu:commandline>
                <qemu:arg value="-object"/>
                <qemu:arg value="memory-backend-file,id=mem,size={$hugepages_memory},mem-path=/dev/hugepages,share=on"/>
                <qemu:arg value="-numa"/>
                <qemu:arg value="node,memdev=mem"/>
                <qemu:arg value="-mem-prealloc"/>
            </qemu:commandline>
        </domain>
    </xsl:template>
</xsl:stylesheet>
