APRIORI DXE {
  INF MdeModulePkg/Core/Dxe/DxeMain.inf
  INF MdeModulePkg/Universal/PCD/Dxe/Pcd.inf

  INF Binaries/x01a/QcomPkg/Drivers/EnvDxe/EnvDxe.inf

  INF MdeModulePkg/Universal/ReportStatusCodeRouter/RuntimeDxe/ReportStatusCodeRouterRuntimeDxe.inf
  INF MdeModulePkg/Universal/StatusCodeHandler/RuntimeDxe/StatusCodeHandlerRuntimeDxe.inf
  INF MdeModulePkg/Core/RuntimeDxe/RuntimeDxe.inf
  INF ArmPkg/Drivers/CpuDxe/CpuDxe.inf
  INF ArmPkg/Drivers/ArmGicDxe/ArmGicDxe.inf
  INF EmbeddedPkg/MetronomeDxe/MetronomeDxe.inf
  INF ArmPkg/Drivers/TimerDxe/TimerDxe.inf

  INF Binaries/x01a/QcomPkg/Drivers/SmemDxe/SmemDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/DALSys/DALSys.inf
  INF Binaries/x01a/QcomPkg/Drivers/HWIODxeDriver/HWIODxeDriver.inf
  INF Binaries/x01a/QcomPkg/Drivers/ChipInfo/ChipInfo.inf
  INF Binaries/x01a/QcomPkg/Drivers/PlatformInfoDxeDriver/PlatformInfoDxeDriver.inf
  INF Binaries/x01a/QcomPkg/Drivers/HALIOMMU/HALIOMMU.inf
  INF Binaries/x01a/QcomPkg/Drivers/ULogDxe/ULogDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/CmdDbDxe/CmdDbDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/PwrUtilsDxe/PwrUtilsDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/NpaDxe/NpaDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/RpmhDxe/RpmhDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/PdcDxe/PdcDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/VcsDxe/VcsDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/ClockDxe/ClockDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/SPMI/SPMI.inf
  INF Binaries/x01a/QcomPkg/Drivers/ShmBridgeDxe/ShmBridgeDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/ScmDxe/ScmDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/DALTLMM/DALTLMM.inf

  INF MdeModulePkg/Universal/ResetSystemRuntimeDxe/ResetSystemRuntimeDxe.inf

  INF Binaries/x01a/QcomPkg/Drivers/PmicDxe/PmicDxe.inf

  INF MdeModulePkg/Universal/Disk/DiskIoDxe/DiskIoDxe.inf
  INF MdeModulePkg/Universal/Disk/PartitionDxe/PartitionDxe.inf
  INF MdeModulePkg/Universal/Disk/UnicodeCollation/EnglishDxe/EnglishDxe.inf

  INF Binaries/x01a/QcomPkg/Drivers/SdccDxe/SdccDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/UFSDxe/UFSDxe.inf

  INF FatPkg/EnhancedFatDxe/Fat.inf

  INF Binaries/x01a/QcomPkg/Drivers/TzDxe/TzDxe.inf

  INF MdeModulePkg/Universal/Variable/RuntimeDxe/VariableRuntimeDxe.inf

  INF Binaries/x01a/QcomPkg/Drivers/FeatureEnablerDxe/FeatureEnablerDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/DDRInfoDxe/DDRInfoDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/I2C/I2C.inf

!if $(USE_CUSTOM_DISPLAY_DRIVER) == 1
  INF Binaries/x01a/QcomPkg/Drivers/DisplayDxe/DisplayDxe.inf
!else
  INF SiliciumPkg/Drivers/SimpleFbDxe/SimpleFbDxe.inf
!endif

  INF Binaries/x01a/QcomPkg/Drivers/PILProxyDxe/PILProxyDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/PILDxe/PILDxe.inf
!if $(USE_CUSTOM_DISPLAY_DRIVER) == 1
  INF Binaries/x01a/QcomPkg/Drivers/CPRDxe/CPRDxe.inf
!endif

  INF MdeModulePkg/Universal/WatchdogTimerDxe/WatchdogTimer.inf
  INF EmbeddedPkg/EmbeddedMonotonicCounter/EmbeddedMonotonicCounter.inf
  INF EmbeddedPkg/RealTimeClockRuntimeDxe/RealTimeClockRuntimeDxe.inf
  INF MdeModulePkg/Universal/PrintDxe/PrintDxe.inf
  INF MdeModulePkg/Universal/DevicePathDxe/DevicePathDxe.inf
  INF MdeModulePkg/Universal/CapsuleRuntimeDxe/CapsuleRuntimeDxe.inf
  INF MdeModulePkg/Universal/HiiDatabaseDxe/HiiDatabaseDxe.inf
  INF MdeModulePkg/Universal/BdsDxe/BdsDxe.inf

  INF Binaries/x01a/QcomPkg/Drivers/AdcDxe/AdcDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/UsbPwrCtrlDxe/UsbPwrCtrlDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/QcomChargerDxeLA/QcomChargerDxeLA.inf
  INF Binaries/x01a/QcomPkg/Drivers/ChargerExDxe/ChargerExDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/UsbfnDwc3Dxe/UsbfnDwc3Dxe.inf

  INF MdeModulePkg/Bus/Usb/UsbBusDxe/UsbBusDxe.inf
  INF MdeModulePkg/Bus/Usb/UsbKbDxe/UsbKbDxe.inf
  INF MdeModulePkg/Bus/Usb/UsbMassStorageDxe/UsbMassStorageDxe.inf

  INF Binaries/x01a/QcomPkg/Drivers/UsbMsdDxe/UsbMsdDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/UsbDeviceDxe/UsbDeviceDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/UsbConfigDxe/UsbConfigDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/ButtonsDxe/ButtonsDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/TsensDxe/TsensDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/LimitsDxe/LimitsDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/GpiDxe/GpiDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/HashDxe/HashDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/CipherDxe/CipherDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/MacDxe/MacDxe.inf
  INF Binaries/x01a/QcomPkg/Drivers/RngDxe/RngDxe.inf

  INF EmbeddedPkg/SimpleTextInOutSerial/SimpleTextInOutSerial.inf
  INF MdeModulePkg/Universal/Console/ConPlatformDxe/ConPlatformDxe.inf
  INF MdeModulePkg/Universal/Console/ConSplitterDxe/ConSplitterDxe.inf
  INF MdeModulePkg/Universal/Console/GraphicsConsoleDxe/GraphicsConsoleDxe.inf

}
