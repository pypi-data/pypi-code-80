import contextlib
import sys

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QSizePolicy, QListView
from matplotlib.axes import Axes

print(rf'''
python is run by {sys.executable}
''')

import sys
import typing

import ismrmrd
import numpy as np
import PySide6
from PySide6.QtCore import Qt, QModelIndex, QItemSelectionModel
from matplotlib.figure import Figure
from PySide6.QtCore import (Property, QAbstractTableModel, QObject,
                            QStringListModel, QUrl, Signal, Slot,
                            qInstallMessageHandler)
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView

from mainwindow import Ui_MainWindow

from matplotlibqml.matplotlibqml import FigureCanvasQTAgg as FigureCanvas

def array_to_str(array_data:list):
    return ','.join(rf'{x}' for x in array_data)
    pass

class DHLTableModel(QAbstractTableModel):
    _fields_ = [("version",                             lambda acqHeader: acqHeader.version),                                  #("version", ctypes.c_uint16),                          
                ("flags",                               lambda acqHeader: acqHeader.flags),                                    #("flags", ctypes.c_uint64),                   
                ("measurement_uid",                     lambda acqHeader: acqHeader.measurement_uid),                          #("measurement_uid", ctypes.c_uint32),                
                ("scan_counter",                        lambda acqHeader: acqHeader.scan_counter),                             #("scan_counter", ctypes.c_uint32),             
                ("acquisition_time_stamp",              lambda acqHeader: acqHeader.acquisition_time_stamp),                   #("acquisition_time_stamp", ctypes.c_uint32),                        
                ("physiology_time_stamp",               lambda acqHeader: array_to_str(acqHeader.physiology_time_stamp)),      #("physiology_time_stamp", ctypes.c_uint32 * PHYS_STAMPS),                            
                ("number_of_samples",                   lambda acqHeader: acqHeader.number_of_samples),                        #("number_of_samples", ctypes.c_uint16),         
                ("available_channels",                  lambda acqHeader: acqHeader.available_channels),                       #("available_channels", ctypes.c_uint16),             
                ("active_channels",                     lambda acqHeader: acqHeader.active_channels),                          #("active_channels", ctypes.c_uint16),         
                ("channel_mask",                        lambda acqHeader: array_to_str(acqHeader.channel_mask)),               #("channel_mask", ctypes.c_uint64 * CHANNEL_MASKS),                     
                ("discard_pre",                         lambda acqHeader: acqHeader.discard_pre),                              #("discard_pre", ctypes.c_uint16),     
                ("discard_post",                        lambda acqHeader: acqHeader.discard_post),                             #("discard_post", ctypes.c_uint16),     
                ("center_sample",                       lambda acqHeader: acqHeader.center_sample),                            #("center_sample", ctypes.c_uint16),     
                ("encoding_space_ref",                  lambda acqHeader: acqHeader.encoding_space_ref),                       #("encoding_space_ref", ctypes.c_uint16),
                ("trajectory_dimensions",               lambda acqHeader: acqHeader.trajectory_dimensions),                    #("trajectory_dimensions", ctypes.c_uint16),
                ("sample_time_us",                      lambda acqHeader: acqHeader.sample_time_us),                           #("sample_time_us", ctypes.c_float),         
                ("position",                            lambda acqHeader: array_to_str(acqHeader.position)),                   #("position", ctypes.c_float * POSITION_LENGTH), 
                ("read_dir",                            lambda acqHeader: array_to_str(acqHeader.read_dir)),                   #("read_dir", ctypes.c_float * DIRECTION_LENGTH),           
                ("phase_dir",                           lambda acqHeader: array_to_str(acqHeader.phase_dir)),                  #("phase_dir", ctypes.c_float * DIRECTION_LENGTH),
                ("slice_dir",                           lambda acqHeader: array_to_str(acqHeader.slice_dir)),                  #("slice_dir", ctypes.c_float * DIRECTION_LENGTH),
                ("patient_table_position",              lambda acqHeader: array_to_str(acqHeader.patient_table_position)),     #("patient_table_position", ctypes.c_float * POSITION_LENGTH),
                ("idx_kspace_encode_step_1",            lambda acqHeader: acqHeader.idx.kspace_encode_step_1),                 #idx ("kspace_encode_step_1", ctypes.c_uint16),
                ("idx_kspace_encode_step_2",            lambda acqHeader: acqHeader.idx.kspace_encode_step_2),                 #idx ("kspace_encode_step_2", ctypes.c_uint16),
                ("idx_average",                         lambda acqHeader: acqHeader.idx.average),                              #idx ("average", ctypes.c_uint16),
                ("idx_slice",                           lambda acqHeader: acqHeader.idx.slice),                                #idx ("slice", ctypes.c_uint16),
                ("idx_contrast",                        lambda acqHeader: acqHeader.idx.contrast),                             #idx ("contrast", ctypes.c_uint16),
                ("idx_phase",                           lambda acqHeader: acqHeader.idx.phase),                                #idx ("phase", ctypes.c_uint16),
                ("idx_repetition",                      lambda acqHeader: acqHeader.idx.repetition),                           #idx ("repetition", ctypes.c_uint16),
                ("idx_set",                             lambda acqHeader: acqHeader.idx.set),                                  #idx ("set", ctypes.c_uint16),
                ("idx_segment",                         lambda acqHeader: acqHeader.idx.segment),                              #idx ("segment", ctypes.c_uint16),
                ("idx_user",                            lambda acqHeader: acqHeader.idx.user),                                 #idx ("user", ctypes.c_uint16 * USER_INTS)]
                ("user_int",                            lambda acqHeader: array_to_str(acqHeader.user_int)),                   #("user_int", ctypes.c_int32 * USER_INTS),
                ("user_float",                          lambda acqHeader: array_to_str(acqHeader.user_float)),                 #("user_float", ctypes.c_float * USER_FLOATS)
    ]
               
    def __init__(self):
        QAbstractTableModel.__init__(self)
        #todo or get when needed?
        self._acqs=[] # None # type: typing.List[ismrmrd.Acquisition]
        pass

    def rowCount(self, parent:PySide6.QtCore.QModelIndex=...) -> int:
        row_count=0 if self._acqs is None else len(self._acqs)
        print(rf'len is {row_count}')
        return row_count
        #return 0 if self._acqs is None else len(self._acqs)
        pass

    def columnCount(self, parent:PySide6.QtCore.QModelIndex=...) -> int:
        row_count=len(DHLTableModel._fields_)
        print(rf'column is {row_count}')
        return  row_count
        pass

    def data(self, index:PySide6.QtCore.QModelIndex, role:int=...) -> typing.Any:
        if not index.isValid():
            return

        if role==QtCore.Qt.DisplayRole or role==QtCore.Qt.ToolTipRole:
            data_value=DHLTableModel._fields_[index.column()][1](self._acqs[index.row()])
            print(rf'try to get role:{role}, index:{index}, data_value:{data_value}')
            return data_value
        else:
            return None

    def headerData(self, section:int, orientation:QtCore.Qt.Orientation, role:int):
        if role==QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation==QtCore.Qt.Orientation.Horizontal:
                return DHLTableModel._fields_[section][0]
            else:
                return rf'{section}'#  line
            pass
        elif role==QtCore.Qt.ItemDataRole.ToolTipRole:
            if orientation==QtCore.Qt.Orientation.Horizontal:
                return DHLTableModel._fields_[section][0]
        return None
        #return PySide6.QtCore.QVariant()
        pass

    def reset_dhls(self, acqs):
        """

        :param dhls: real dhls
        :return:
        """

        if acqs is not self._acqs:
            print(rf'new acqs')
            self.beginResetModel()
            self._acqs=acqs
            self.endResetModel()
        else:
            print(rf'warning: try to reset dhls with the old one!')
        pass
    pass

class AppViewModel(QObject):
    #select_line_changed=Signal(int)
    #select_point_changed=Signal(int)

    #  当前数据列表的值
    #currentLineListModelChanged=Signal()
    # 当前选中项
    #tableModelSelectIndexChanged=Signal()
    def __init__(self):
        QObject.__init__(self)

        self._tableModel=DHLTableModel()
        #self._slectionModel=self.
        #self._currentList=None  # type: QStringListModel
        self._channelCount=0 # type: int
        self._active_channel=0 # type: int
        self._figure=None # type: Figure
        #self._tableModelSelectIndex=0 #

        self._acqs=[]    # type: typing.List[ismrmrd.Acquisition]

        # 当前行/当前通道原始数据
        self._currentLineData=None # type: np.array

        # 当前行用于渲染的数据
        self._currentLineListModel=QStringListModel() # type: QStringListModel
        #self._currentLineListModel.setStringList(['1','2','3'])

        #self.channelCountChanged.connect(self.safe_update_list_model)
        #self.currentChannelIndexChanged.connect(self.safe_update_list_model)


        self._canvas=None # type: FigureCanvas
        self._figure=None # type: Figure
        self._axes=None

        self._tableview=None # type: QTableView

        self._selectionModel=None # type: QItemSelectionModel

        self._listview=None # type: QListView
        self._listViewSelectionModel=None # type: QItemSelectionModel
        self._tableModelSelectIndex=0 # ?
        self.stop_update_whole_view=False # global backend data fix in progress
        self.stop_update_list_data=False

        pass

    @property
    def tableModel(self):
        return self._tableModel
        pass

    # figure
    def update_canvas(self, canvas):
        # if self._figure != figure:
        #     self._figure=figure
        #     self.update_view()
        #     pass
        self._canvas=canvas
        self._figure=self._canvas.figure
        self._axes = self._figure.subplots(2, 2, sharex='all')
        pass

    def update_tableview(self, tableview: QTableView):
        self._tableview=tableview
        self._tableview.setModel(self._tableModel)
        self._selectionModel=self._tableview.selectionModel()

        self._selectionModel.currentRowChanged.connect(self.on_tableview_currentRowChanged)

        pass

    def update_listview(self, listView: QListView):
        self._listview=listView
        self._listview.setModel(self._currentLineListModel)
        self._listViewSelectionModel=self._listview.selectionModel()
        self._listViewSelectionModel.currentRowChanged.connect(self.on_listview_point_select)
        pass
    def on_tableview_currentRowChanged(self, current: QModelIndex, previous:QModelIndex):
        if current.isValid():
            row=current.row()
            self._on_currentListDataChanged(self._acqs[row])
            pass
        pass

    def on_listview_point_select(self, current: QModelIndex, previous:QModelIndex):
        if current.isValid():
            row=current.row()
            print(rf'some point be selected {row}')
            #todo sync with four axes and right list?
            #save to local ?
            #self._on_currentListDataChanged(self._acqs[row])
            pass
        pass
    
    def _on_currentListDataChanged(self, newAcq:ismrmrd.Acquisition):
        if self._currentLineData is not newAcq.data:
            self._currentLineData=newAcq.data
            header=newAcq.getHead() # type: ismrmrd.AcquisitionHeader
            #channelNum=getattr(header, 'active_channels')
            channelNum = header.active_channels

            with self.stop_update_scope():
                old_active_channel=self._active_channel
                self.on_channelCountChanged(channelNum)
                if old_active_channel < channelNum :
                    #self.on_active_channel_changed(old_active_channel)
                    self._active_channel=old_active_channel
                    pass

            #self.update_view()
            #how about active channel
        pass

    #--begin-- active channel
    activeChannelChangedSignal=Signal(int) # use to notify ui?
    @Slot(int)
    def activeChannelChangeSlot(self, new_active_channel:int):
        self.on_active_channel_changed(new_active_channel)
        pass

    def on_active_channel_changed(self, new_active_channel:int):
        if not self._active_channel==new_active_channel and new_active_channel<self._channelCount:
            self._active_channel=new_active_channel
            self.activeChannelChangedSignal.emit(new_active_channel)
            #self.safe_update_list_model()
            self.update_view()
            pass
        pass

    @Slot(int)
    def SetActiveChannel(self, new_active_channel:int):
        self.on_active_channel_changed(new_active_channel)
        pass
    #--end-- active channel

    channelCountChangedSignal=Signal(int)
    def on_channelCountChanged(self, newChannelNum:int):
        if newChannelNum != self._channelCount:
            self._channelCount=newChannelNum
            self.channelCountChangedSignal.emit(newChannelNum)
        pass

    def open_file(self, file_path:str):
      
        dataset=ismrmrd.Dataset(file_path)
        self._acqs=[]
        for i in range(dataset.number_of_acquisitions()):
            self._acqs.append(dataset.read_acquisition(i))

        with self.stop_update_scope():
            self._tableModel.reset_dhls(self._acqs)
        #self.update_view()
        pass

    @contextlib.contextmanager
    def stop_update_scope(self):
        self.stop_update_whole_view=True
        yield
        self.stop_update_whole_view=False
        self.update_view()

    def update_view(self):
        """
            1. 更新绘图面板
            2. 更新数据列表

        :return:
        """

        if self.stop_update_whole_view:
            return

        if self._figure==None:
            print(rf'_figure is None')
            return

        if self._channelCount is None or self._channelCount<0:
            print(rf'channel count less than 0: {self._channelCount}')
            return
            pass

        if self.tableModel==None:
            print(rf'table model is None')
            return
            pass

        if self._tableModelSelectIndex<0 or self._tableModelSelectIndex > self.tableModel.rowCount():
            print(rf'table model select index out of range, tableModelSelectIndex:{ self._tableModelSelectIndex}, tableModelRowCount:{self.tableModel.rowCount()}')
            return
            pass

        if self._acqs is None:
            print(rf'dls is None')
            return
            pass

        # self.pull_list_value()
        # self.draw_impl()

        self.safe_update_list_model()

        self.safe_draw_matplotlib()

        pass


    # @contextlib.contextmanager
    # def update_list_model_paritial_state(self):
    #     self.stop_update_list_data=True
    #     yield
    #     self.stop_update_list_data=False
    #     self.safe_update_list_model()

    def safe_update_list_model(self):
        #if not self.stop_update_list_data:
        acq=self._acqs[self._tableModelSelectIndex]
        self._currentLineData=acq.data[self._active_channel-1, :] # type: typing.List[np.complex64]
        #self._currentLineListModel.clearItemData()
        self._currentLineListModel.setStringList([ rf'{c.real}, {c.imag}' for c in self._currentLineData])
        pass

    @Slot()
    def safe_draw_matplotlib(self):
        axes=self._axes # type: typing.Tuple[typing.Tuple[Axes, Axes],typing.Tuple[Axes, Axes]]
        (ax_real, ax_img), (ax_mag, ax_phase)=axes

        ax_real.clear()
        ax_real.set_title('Real')
        ax_real.plot(np.real(self._currentLineData))
        #ax_real.plot([1,2,3,4,5])
        ax_img.clear()
        ax_img.set_title('Image')
        ax_img.plot(np.imag(self._currentLineData))

        ax_mag.clear()
        ax_mag.set_title('Mag')
        ax_mag.plot(np.abs(self._currentLineData))

        #self._figure.show()
        ax_phase.clear()
        ax_phase.set_title('Phase')
        ax_phase.plot(np.angle(self._currentLineData))
        #self._figure.canvas
        #self._canvas.update()
        #self._figure.tight_layout()
        #self._canvas.resizeEvent()
        dpi=100
        #self._canvas.setFixedSize(self._canvas.parent().size())
        self._figure.set_size_inches(self._canvas.width()/dpi, self._canvas.height()/dpi)
        self._figure.set_dpi(dpi)
        self._figure.tight_layout()
        self._canvas.draw_idle()



        pass

    pass


class MainWindow(QMainWindow):
    # @Slot()
    # def on_action_open_clicked(self):
    #     pass

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        figure=Figure()
        canvas=FigureCanvas(figure, None)
        canvas.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.ui.linePlotsFrame.layout().addWidget(canvas)

        #TODO how to make ui designer to support it?
        #self.ui.linePlotsFrame.children().append(canvas)
        #self.ui.linePlotsFrame.addWidget(canvas)
        print('before new model')
        self.vm=AppViewModel()

        #self.ui.acqHeaderTableView.setModel(self.vm.tableModel)
        print('before update canvas')
        self.vm.update_canvas(canvas)
        self.vm.update_tableview(self.ui.acqHeaderTableView)
        print('before trigger')

        self.vm.channelCountChangedSignal.connect(self.ui.activeChannelSlider.setMaximum)
        self.ui.activeChannelSlider.valueChanged.connect(self.vm.activeChannelChangeSlot)


        self.vm.update_listview(self.ui.currentDataListView)
        #self.ui.actionOpen.triggered.connect(self.on_actionOpen_triggered)
        #self.ui.actionOpen.connect(vm.open_file())

        # how about the action?
        # connect open and fix other one by one
        # do something for logical?
    @Slot()
    def on_actionOpen_triggered(self):
        print('do trigger')
        #file_name, file_filter=QtWidgets.QFileDialog.getOpenFileName(self,
        #        "Open Image", ".", "H5 Files (*.h5 *.raw)")
        file_name='/home/congzhang/work/testdata.h5'
        self.vm.open_file(file_name)
        pass

def main(argv: typing.List[str]):
    qInstallMessageHandler(lambda x, y, msg: print(msg))

    #vm=AppViewModel()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    # 
    # view=QListView()
    # model=QStringListModel(['1','2'])
    # view.setModel(model)
    # 
    # model.setStringList(['4','5'])
    # view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))