function change(){

    var milasUrl={};//新建对象，用来存储所有数据
    var subMilasUrlArr={};//存储每一行数据
    var tableData={};
    var list=[];
    var table_name=$('#table_name').text()
    var table_comment=$('#table_comment').val()

    console.log(table_name)
    console.log(table_comment)

     $(".table tbody tr").each(function(trindex,tritem){//遍历每一行
         tableData[trindex]=new Array();

      $(tritem).find("input").each(function(tdindex,tditem){
          tableData[trindex][tdindex]=$(tditem).val();//遍历每一个数据，并存入

          //subMilasUrlArr[trindex]=tableData[trindex];//将每一行的数据存入
      });
  });
     for(var key in subMilasUrlArr)
     {
         milasUrl[key]=subMilasUrlArr[key];//将每一行存入对象
     }
    tableData=JSON.stringify(tableData)
    console.log(tableData)
    var choice=confirm('确认修改?')

    if (choice){
        $.ajax({
            url:'/table_comment_edit/',
            data:{table_info:table_comment,col_info:tableData,table_name:table_name},
            type:'POST',
            beforeASend:function () {
                console.log('111')
                $("#loadingModal").modal('show');
            },
            success:function (data) {
                console.log(data)
                if (data=='success'){
                    toastr.success('提交数据成功');
                }
                else if (data=='error'){
                    toastr.warning('出错了>_<');
                }

            }
        })
    }

}
