#
# hello-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

#
# hello-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#
import io
import json
import time
from fdk import response
import oci
from oci.data_integration.data_integration_client import DataIntegrationClient
def handler(ctx, data: io.BytesIO=None):
  signer = oci.auth.signers.get_resource_principals_signer()
  body = json.loads(data.getvalue())
  resource_name = body["data"]["resourceName"]
  resp = do(signer,resource_name)
  return response.Response(
    ctx, response_data=resp,
    headers={"Content-Type": "application/json"}
  )
def do(signer, objectName):
  dip = DataIntegrationClient(config={}, signer=signer)
  wsid = "ocid1.disworkspace.oc1.iad.anuwcljs2ow634yaf2tosblbf36ajfd64xgi4537l7yfpt3e54ya5qzsfoca"
  application="ocid1.disapplication.oc1.iad.amaaaaaa2ow634yajxveokg2tv3j5mfypaqx7kfhd5arewov5izctee6sskq"
  task="797b866c-4959-4093-8a7c-2c8b341387b1"
  md = oci.data_integration.models.RegistryMetadata(aggregator_key=task)
  trkey = str(int(time.time()))
  #cp={"bindings":{"SRCDATAPARAM":{"rootObjectValue":{"modelType":"ENRICHED_ENTITY","entity":{"modelType":"FILE_ENTITY","key":"dataref:37bed599-997d-4da2-b0a9-cccccc46ec5b/disdemodata/FILE_ENTITY:"+objectName, "externalKey":"https://objectstorage.us-ashburn-1.oraclecloud.com/myosnamespace/disdemodata/"+objectName, "objectStatus" : 1},"dataFormat":{"formatAttribute":{"modelType":"JSON_FORMAT","encoding":"UTF-8"},"type":"JSON"}}}}}
  task = oci.data_integration.models.CreateTaskRunDetails(key=trkey, registry_metadata=md)
  tsk = dip.create_task_run(wsid,application, create_task_run_details=task)
  print(tsk.data)
  return tsk.data
