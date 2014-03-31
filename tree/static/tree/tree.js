    var Tree = function(urlpath) {
      this.t;

	var setting = {
	    async: {
	        enable: true,
	        url: '',
	        autoParam:["id","name"]
	    },
		view: {
			dblClickExpand: false,
			showLine: true,
			selectedMulti: false
		},
		edit: {
                enable: true,
				showRemoveBtn: false,
				showRenameBtn: false,
		    drag:{isCopy:false,isMove:true,prev:true,inner:true,next:true}
		    },
		data: {
			simpleData: {
				enable:true,
				idKey: "id",
				pIdKey: "pId",
				rootPId: ""
			}
		},
		callback: {
			}
		
	};

      setting.async.url = urlpath.nodes;
      var that = this;
      that.setting = setting;
      var urls = urlpath
      this.addDiyDom = function (treeId, treeNode) {
                var aObj = $("#" + treeNode.tId + "_a");
                if ($("#diyBtn_"+treeNode.id).length>0) return;

                if (treeNode.id!=-1)
                    {
	                var editStr = "<span> </span>"
		                + "<button type='button' class='tree_editBtn' id='tree_editBtn_" + treeNode.id
		                + "' title='"+treeNode.name+"' onfocus='this.blur();'></button>"
		                +"<span> </span>"
		                + "<button type='button' class='tree_newBtn' id='tree_newBtn_" + treeNode.id
		                + "' title='"+treeNode.name+"' onfocus='this.blur();'></button>"
   		                +"<span> </span>"
		                + "<button type='button' class='tree_removeBtn' id='tree_removeBtn_" + treeNode.id
		                + "' title='"+treeNode.name+"' onfocus='this.blur();'></button>"
   		                +"<span> </span>"
		                + "<button type='button' class='tree_infoBtn' id='tree_infoBtn_" + treeNode.id
		                + "' title='"+treeNode.name+"' onfocus='this.blur();'></button>";
		                
	            }
	            else {
	                var editStr = "<span> </span>"
		                + "<button type='button' class='tree_newBtn' id='tree_newBtn_" + treeNode.id
		                + "' title='"+treeNode.name+"' onfocus='this.blur();'></button>";
	            
	            }
	                aObj.append(editStr);
	                var btn = $("#tree_editBtn_"+treeNode.id);
	                if (btn) btn.bind("click", function(){
	                                                   that.t.selectNode(treeNode);
	                                                   that.t.editName(treeNode);
	                                });

	                var btn = $("#tree_newBtn_"+treeNode.id);
	                if (btn) btn.bind("click", function(){that.addNode(treeNode);});

	                var btn = $("#tree_removeBtn_"+treeNode.id);
	                if (btn) btn.bind("click", function(){that.delNode(treeNode);});

        };

      this.addNode = function(parent) {
//         console.log('parent',parent);
         var ansver=prompt("Enter node name");
         if (ansver!=null) {
            var newNode = {name:ansver, isParent:false}; //, pId:parent.id
            var url=urls['addNode']+'?parent='+parent.id+'&name='+ansver;
            $.ajax({
                url: url,
                success:function (data){ 
                              newNode.id = data.node_id;
                              if (data.status=='Ok'){
                                    if (parent.isParent==false) {
                                        parent.isParent=true;
                                        that.t.updateNode(parent);
                                        }
                                    that.t.addNodes(parent, newNode);
                              }
                              else {    
                                alert('Server error');
                                console.log("returned,", data);
                              }
                      }
                });
          }
      }
      
      this.renameNode = function (treeId, node, newName, isCancel) {
        if(isCancel!=true && node.name!=newName) {
            var oldname = node.name;
            var url=urls['editNode']+'?node='+node.id+'&name='+newName;
            $.ajax({
                url: url,
                success:function (data){ 
                              if (data.status!='Ok'){
                                alert('Server error');
                                console.log("returned,", data);
                                node.name=oldname;
                                that.t.updateNode(node);
                              }
                      }
                });
            return true; //rename itself when server return error
            }
        }

      this.delNode = function (node) {
            if (confirm("Delete this node and ALL subnodes?")==true) {
                var url=urls['delNode']+'?node='+node.id;
                $.ajax({
                    url: url,
                    success:function (data){ 
                                  if (data.status!='Ok'){
                                    alert('Server error');
                                    console.log("returned,", data);
                                  }
                                  else {
                                    that.t.removeNode(node);
                                  }
                          }
                    });
             }   
        }

      this.beforeDrag = function (treeId, treeNodes) {
//            if (treeNodes[0].id!=-1)
			return treeNodes[0].id!=-1;
		}
	  this.beforeDrop = function (treeId, treeNodes, targetNode, moveType) {
	        console.log(treeId, treeNodes, targetNode, moveType);
	        var url=urls['moveNode']+'?node='+treeNodes[0].id+'&target='+targetNode.id+'&movetype='+moveType;
                $.ajax({
                    url: url,
                    success:function (data){ 
                                  if (data.status!='Ok'){
                                    alert('Server error');
                                    console.log("returned,", data);
                                  }

                          }
                    });
			return true;
		}
		
      this.init = function (dom_id,setting){
        var t = $(dom_id);
        that.setting.view.addDiyDom=this.addDiyDom;
        that.setting.callback.beforeRename = this.renameNode;
        that.setting.callback.beforeDrag = this.beforeDrag;
        that.setting.callback.beforeDrop = this.beforeDrop;
		t = $.fn.zTree.init(t, that.setting);
		this.t = t;
      }
    };

