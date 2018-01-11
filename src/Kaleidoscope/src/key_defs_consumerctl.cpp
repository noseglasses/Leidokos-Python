/* -*- mode: c++ -*-
 * Leidokos-Python -- Wraps Kaleidoscope modules' c++
 *    code to be available in Python programs.
 * Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "Leidokos-Python.h"

#include "key_defs_consumerctl.h"

namespace kaleidoscope {
namespace python {

#define FOR_ALL_CONSUMER_CTL(FUNC) \
FUNC(NumericKeyPad) \
FUNC(ProgrammableButtons) \
FUNC(MicrophoneCa) \
FUNC(HeadphoneCa) \
FUNC(GraphicEqualizerCa) \
\
FUNC(Plus10) \
FUNC(Plus100) \
FUNC(AMSlashPM) \
\
FUNC(Power) \
FUNC(Reset) \
FUNC(Sleep) \
FUNC(Sleep_After) \
FUNC(Sleep_Mode) \
FUNC(Illumination) \
FUNC(Function_Buttons) \
\
FUNC(Menu) \
FUNC(MenuPick) \
FUNC(MenuUp) \
FUNC(MenuDown) \
FUNC(MenuLeft) \
FUNC(MenuRight) \
FUNC(MenuEscape) \
FUNC(MenuValueIncrease) \
FUNC(MenuValueDecrease) \
\
FUNC(DataOnScreen) \
FUNC(ClosedCaption) \
FUNC(ClosedCaptionSelect) \
FUNC(VCRSlashTV) \
FUNC(BroadcastMode) \
FUNC(SNapshot) \
FUNC(Still) \
\
FUNC(Selection) \
FUNC(AssignSelection) \
FUNC(ModeStep) \
FUNC(RecallLast) \
FUNC(EnterChannel) \
FUNC(OrderMovie) \
FUNC(Channel) \
FUNC(MediaSelection) \
FUNC(MediaSelectComputer) \
FUNC(MediaSelectTV) \
FUNC(MediaSelectWww) \
FUNC(MediaSelectDvd) \
FUNC(MediaSelectTelephone) \
FUNC(MediaSelectProgramGuide) \
FUNC(MediaSelectVideoPhone) \
FUNC(MediaSelectGames) \
FUNC(MediaSelectMessages) \
FUNC(MediaSelectCd) \
FUNC(MediaSelectVcr) \
FUNC(MediaSelectTuner) \
FUNC(Quit) \
FUNC(Help) \
FUNC(MediaSelectTape) \
FUNC(MediaSelectCable) \
FUNC(MediaSelectSatellite) \
FUNC(MediaSelectSecurity) \
FUNC(MediaSelectHome) \
FUNC(MediaSelectCall) \
FUNC(ChannelIncrement) \
FUNC(ChannelDecrement) \
FUNC(MediaSelectSap) \
\
FUNC(VcrPlus) \
FUNC(Once) \
FUNC(Daily) \
FUNC(Weekly) \
FUNC(Monthly) \
\
FUNC(Play) \
FUNC(Pause) \
FUNC(Record) \
FUNC(FastForward) \
FUNC(Rewind) \
FUNC(ScanNextTrack) \
FUNC(ScanPreviousTrack) \
FUNC(Stop) \
FUNC(Eject) \
FUNC(RandomPlay) \
FUNC(SelectDisc) \
FUNC(EnterDiscMc) \
FUNC(Repeat) \
FUNC(Tracking) \
FUNC(Track_Normal) \
FUNC(SlowTracking) \
FUNC(FrameForward) \
FUNC(FrameBack) \
FUNC(Mark) \
FUNC(ClearMark) \
FUNC(RepeatFromMark) \
FUNC(ReturnTo_Mark) \
FUNC(SearchMarkForward) \
FUNC(SearchMarkBackwards) \
FUNC(CounterReset) \
FUNC(ShowCounter) \
FUNC(TrackingIncrement) \
FUNC(TrackingDecrement) \
FUNC(StopSlashEject) \
FUNC(PlaySlashPause) \
FUNC(PlaySlashSkip) \
FUNC(Volume) \
FUNC(Balance) \
FUNC(Mute) \
FUNC(Bass) \
FUNC(Treble) \
FUNC(BassBoost) \
FUNC(SurroundMode) \
FUNC(Loudness) \
FUNC(Mpx) \
FUNC(VolumeIncrement) \
\
FUNC(VolumeDecrement) \
\
FUNC(SpeedSelect) \
FUNC(PlaybackSpeed) \
FUNC(StandardPlay) \
FUNC(LongPlay) \
FUNC(ExtendedPlay) \
FUNC(Slow) \

// The following definitions are ill formed (see https://github.com/keyboardio/Kaleidoscope/issues/263)

/*
FUNC(FanEnable) \
FUNC(FanSpeed) \
FUNC(LightEnable) \
FUNC(LightIlluminationLevel) \
FUNC(ClimateControlEnable) \
FUNC(RoomTemperature) \
FUNC(SecurityEnable) \
FUNC(FireAlarm) \
FUNC(PoliceAlarm) \
FUNC(Proximity) \
FUNC(Motion) \
FUNC(DuressAlarm) \
FUNC(HoldupAlarm) \
FUNC(MedicalAlarm) \
\
FUNC(BalanceRight) \
FUNC(BalanceLeft) \
FUNC(BassIncrement) \
FUNC(BassDecrement) \
FUNC(TrebleIncrement) \
FUNC(TrebleDecrement) \
\
FUNC(SpeakerSystem) \
FUNC(ChannelLeft) \
FUNC(ChannelRight) \
FUNC(ChannelCenter) \
FUNC(ChannelFront) \
FUNC(ChannelCenterFront) \
FUNC(ChannelSide) \
FUNC(ChannelSurround) \
FUNC(ChannelLowFrequencyEnhancement) \
FUNC(ChannelTop) \
FUNC(ChannelUnknown) \
\
FUNC(SubChannel) \
FUNC(SubChannelIncrement) \
FUNC(SubChannelDecrement) \
FUNC(AlternateAudioIncrement) \
FUNC(AlternateAudioDecrement) \
\
FUNC(Application_Launch_Buttons) \
FUNC(AL_Launch_Button_Configuration_Tool) \
FUNC(AL_Programmable_Button_Configuration) \
FUNC(AL_Consumer_Control_Configuration) \
FUNC(AL_Word_Processor) \
FUNC(AL_Text_Editor) \
FUNC(AL_Spreadsheet) \
FUNC(AL_Graphics_Editor) \
FUNC(AL_Presentation_App) \
FUNC(AL_Database_App) \
FUNC(AL_Email_Reader) \
FUNC(AL_Newsreader) \
FUNC(AL_Voicemail) \
FUNC(AL_Contacts_Slash_Address_Book) \
FUNC(AL_Calendar_Slash_Schedule) \
FUNC(AL_Task_Slash_Project_Manager) \
FUNC(AL_Log_Slash_Journal_Slash_Timecard) \
FUNC(AL_Checkbook_Slash_Finance) \
FUNC(AL_Calculator) \
FUNC(AL_AVCaptureSlashPlayback) \
FUNC(AL_Local_MachineBrowser) \
FUNC(AL_Lan_SlashWanBrowser) \
FUNC(AL_InternetBrowser) \
FUNC(AL_RemoteNetworkingSlashIspConnect) \
FUNC(AL_NetworkConference) \
FUNC(AL_NetworkChat) \
FUNC(AL_TelephonySlashDialer) \
FUNC(AL_Logon) \
FUNC(AL_Logoff) \
FUNC(AL_LogonSlashLogoff) \
FUNC(AL_TerminalLockSlashScreensaver) \
FUNC(AL_ControlPanel) \
FUNC(AL_CommandLineProcessorSlashRun) \
FUNC(AL_ProcessSlashTask_Manager) \
FUNC(AL_SelectTaskSlashApplication) \
FUNC(AL_NextTaskSlashApplication) \
FUNC(AL_PreviousTaskSlashApplication) \
FUNC(AL_PreemptiveHaltTaskSlashApplication) \
FUNC(AL_IntegratedHelpCenter) \
FUNC(AL_Documents) \
FUNC(AL_Thesaurus) \
FUNC(AL_Dictionary) \
FUNC(AL_Desktop) \
FUNC(AL_SpellCheck) \
FUNC(AL_GrammarCheck) \
FUNC(AL_WirelessStatus) \
FUNC(AL_KeyboardLayout) \
FUNC(AL_VirusProtection) \
FUNC(AL_Encryption) \
FUNC(AL_ScreenSaver) \
FUNC(AL_Alarms) \
FUNC(AL_Clock) \
FUNC(AL_FileBrowser) \
FUNC(AL_PowerStatus) \
FUNC(AL_ImageBrowser) \
FUNC(AL_AudioBrowser) \
FUNC(AL_MovieBrowser) \
FUNC(AL_DigitalRightsManager) \
FUNC(AL_DigitalWallet) \
\
FUNC(AL_InstantMessaging) \
FUNC(AL_OemFeaturesSlashTipsSlashTUTORIALBrowser) \
FUNC(AL_OemHelp) \
FUNC(AL_OnlineCommunity) \
FUNC(AL_Entertainment_Content_Browser) \
FUNC(AL_OnlineShoppingBrowser) \
FUNC(AL_SmartcardInformationSlashHelp) \
FUNC(AL_MarketMonitorSlashFinanceBrowser) \
FUNC(AL_CustomizedCorporateNewsBrowser) \
FUNC(AL_OnlineActivityBrowser) \
FUNC(AL_ResearchSlashSearchBrowser) \
FUNC(AL_AudioPlayer) \
\
FUNC(GenericGuiApplicationControls) \
FUNC(AC_New) \
FUNC(AC_Open) \
FUNC(AC_Close) \
FUNC(AC_Exit) \
FUNC(AC_Maximize) \
FUNC(AC_Minimize) \
FUNC(AC_Save) \
FUNC(AC_Print) \
FUNC(AC_Properties) \
FUNC(AC_Undo) \
FUNC(AC_Copy) \
FUNC(AC_Cut) \
FUNC(AC_Paste) \
FUNC(AC_SelectAll) \
FUNC(AC_Find) \
FUNC(AC_FindAndReplace) \
FUNC(AC_Search) \
FUNC(AC_GoTo) \
FUNC(AC_Home) \
FUNC(AC_Back) \
FUNC(AC_Forward) \
FUNC(AC_Stop) \
FUNC(AC_Refresh) \
FUNC(AC_PreviousLink) \
FUNC(AC_NextLink) \
FUNC(AC_Bookmarks) \
FUNC(AC_History) \
FUNC(AC_Subscriptions) \
FUNC(AC_ZoomIn) \
FUNC(AC_ZoomOut) \
FUNC(AC_Zoom) \
FUNC(AC_FullSCreenView) \
FUNC(AC_NormalView) \
FUNC(AC_ViewToggle) \
FUNC(AC_ScrollUp) \
FUNC(AC_ScrollDown) \
FUNC(AC_Scroll) \
FUNC(AC_PanLeft) \
FUNC(AC_PanRight) \
FUNC(AC_Pan) \
FUNC(AC_NewWindow) \
FUNC(AC_TileHorizontally) \
FUNC(AC_TileVertically) \
FUNC(AC_Format) \
FUNC(AC_Edit) \
FUNC(AC_Bold) \
FUNC(AC_Italics) \
FUNC(AC_Underline) \
FUNC(AC_Strikethrough) \
FUNC(AC_Subscript) \
FUNC(AC_Superscript) \
FUNC(AC_AllCaps) \
FUNC(AC_Rotate) \
FUNC(AC_Resize) \
FUNC(AC_FlipHorizontal) \
FUNC(AC_FlipVertical) \
FUNC(AC_MirrorHorizontal) \
FUNC(AC_MirrorVertical) \
FUNC(AC_FontSelect) \
FUNC(AC_FontColor) \
FUNC(AC_FontSize) \
FUNC(AC_JustifyLeft) \
FUNC(AC_JustifyCenterH) \
FUNC(AC_JustifyRight) \
FUNC(AC_JustifyBlockH) \
FUNC(AC_JustifyTop) \
FUNC(AC_JustifyCenterV) \
FUNC(AC_JustifyBottom) \
FUNC(AC_JustifyBlockV) \
FUNC(AC_IndentDecrease) \
FUNC(AC_IndentIncrease) \
FUNC(AC_NumberedList) \
FUNC(AC_RestartNumbering) \
FUNC(AC_BulletedList) \
FUNC(AC_Promote) \
FUNC(AC_Demote) \
FUNC(AC_Yes) \
FUNC(AC_No) \
FUNC(AC_Cancel) \
FUNC(AC_Catalog) \
FUNC(AC_BuySlashCheckout) \
FUNC(AC_AddToCart) \
FUNC(AC_Expand) \
FUNC(AC_ExpandAll) \
FUNC(AC_Collapse) \
FUNC(AC_CollapseAll) \
FUNC(AC_PrintPreview) \
FUNC(AC_PasteSpecial) \
FUNC(AC_InsertMode) \
FUNC(AC_Delete) \
FUNC(AC_Lock) \
FUNC(AC_Unlock) \
FUNC(AC_Protect) \
FUNC(AC_Unprotect) \
FUNC(AC_AttachComment) \
FUNC(AC_DeleteComment) \
FUNC(AC_ViewComment) \
FUNC(AC_SelectWord) \
FUNC(AC_SelectSentence) \
FUNC(AC_SelectParagraph) \
FUNC(AC_SelectColumn) \
FUNC(AC_SelectRow) \
FUNC(AC_SelectTable) \
FUNC(AC_SelectObject) \
FUNC(AC_RedoSlashRepeat) \
FUNC(AC_Sort) \
FUNC(AC_Sort_Ascending) \
FUNC(AC_Sort_Descending) \
FUNC(AC_Filter) \
FUNC(AC_SetClock) \
FUNC(AC_ViewClock) \
FUNC(AC_SelectTimeZone) \
FUNC(AC_EditTimeZones) \
FUNC(AC_SetAlarm) \
FUNC(AC_ClearAlarm) \
FUNC(AC_SnoozeAlarm) \
FUNC(AC_ResetAlarm) \
FUNC(AC_Synchronize) \
FUNC(AC_SendSlashReceive) \
FUNC(AC_SendTo) \
FUNC(AC_Reply) \
FUNC(AC_ReplyAll) \
FUNC(AC_ForwardMsg) \
FUNC(AC_Send) \
FUNC(AC_AttachFile) \
FUNC(AC_Upload) \
FUNC(AC_Download) \
FUNC(AC_SetBorders) \
FUNC(AC_InsertRow) \
FUNC(AC_InsertColumn) \
FUNC(AC_InsertFile) \
FUNC(AC_InsertPicture) \
FUNC(AC_InsertObject) \
FUNC(AC_InsertSymbol) \
FUNC(AC_SaveandClose) \
FUNC(AC_Rename) \
FUNC(AC_Merge) \
FUNC(AC_Split) \
FUNC(AC_Distribute_Horizontally) \
FUNC(AC_Distribute_Vertically)
*/
   
#define DEFINE_CONSUMER_CTL(KEY) \
   static Key_ cctl_##KEY() { return Consumer_##KEY; }
   
FOR_ALL_CONSUMER_CTL(DEFINE_CONSUMER_CTL)

static void initPythonStuff() {
   
   #define EXPORT_CONSUMER_CTL(KEY) \
      boost::python::def("keyConsumer"#KEY, &kaleidoscope::python::cctl_##KEY, \
         "Returns the consumer control key \"" #KEY "\".\n\n" \
         "Returns:\n" \
         "   Key: The consumer control key \"" #KEY "\"." \
      );
      
   FOR_ALL_CONSUMER_CTL(EXPORT_CONSUMER_CTL)
}
      
KALEIDOSCOPE_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
