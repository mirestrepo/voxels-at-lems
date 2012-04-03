# Script to register the dbrec3d manager
# Author : Isabel Restrepo
#6-21-2010



print("Register Managers");
dbrec3d_batch.init_process("dbrec3dRegisterManagersProcess");
dbrec3d_batch.run_process();
(id, type) = dbrec3d_batch.commit_output(0);
parts_manager= dbvalue(id, type);
(id, type) = dbrec3d_batch.commit_output(1);
context_manager= dbvalue(id, type);