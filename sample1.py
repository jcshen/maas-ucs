'''
1. how to list all of the server profiles created, and obtain information such as mac address
2. how to power control them, either via creating ipmi service profile/applying the setting or directly via api call
3. how to tell the blade to pxe boot via api call
'''

from UcsSdk import *

def list_all_service_profiles(handle):
    '''
        This will list all the service profiles under org-root
        and print out :
          Name
          Dn ( absoulute location of the tree ) 
          Uuid
    '''
    rsp = handle.GetManagedObject(None, None,{"Dn":"org-root"})
    rsp = handle.GetManagedObject(rsp, "lsServer",{"Type":"instance"}, inHierarchical=False)
    for sp in rsp:
        print "Service Profile Name :{:<20}, Dn : {:<30}, Uuid : {:<30}".format(sp.Name, sp.Dn, sp.Uuid)
         
       

def list_mac_address_of_all_service_profiles(handle, sp_name = None):
    '''
        This will query print all mac address for each vnic of service profile
        Please note the "handle.[Start|Complete]Transaction" 
    '''
    handle.StartTransaction()
    rsp = handle.GetManagedObject(None, None,{"Dn":"org-root"})
    rsp = handle.GetManagedObject(rsp, "lsServer",{"Type":"instance","Name":sp_name}, inHierarchical=False)
    rsp = handle.GetManagedObject(rsp, "vnicEther",{}, inHierarchical=False)
    handle.CompleteTransaction()
    
    for vnic in rsp:
        print "Vnic Name : [{}] , Dn : [{}], Address : [{}]".format(vnic.Name, vnic.Dn, vnic.Addr )

        
def find_sp_by_mac_addr(handle, mac_addr):
    '''
        This will return the Service Profile Dn ( Absolute "address" in the MO tree )
        contain the mac address specified 
    '''
    handle.StartTransaction()
    rsp = handle.GetManagedObject(None, None,{"Dn":"org-root"})
    rsp = handle.GetManagedObject(rsp, "lsServer",{"Type":"instance"}, inHierarchical=False)
    rsp = handle.GetManagedObject(rsp, "vnicEther",{"Addr":mac_addr}, inHierarchical=True)
    handle.CompleteTransaction()
    
    if len(rsp) == 0 :
        print "No vnic found "
    for vnic in rsp:
        print "Vnic Name : [{}] , Dn : [{}], Address : [{}]".format(vnic.Name, vnic.Dn, vnic.Addr )
    
if __name__ == "__main__":
    try :
        handle = UcsHandle()
        handle.Login("10.193.159.76","admin","Nbv12345")    
        list_all_service_profiles(handle)
        list_mac_address_of_all_service_profiles(handle)
        find_sp_by_mac_addr(handle, r'00:25:B5:A1:17:01')
        
    finally:
        handle.Logout()
