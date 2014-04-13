'''
1. how to list all of the server profiles created, and obtain information such as mac address
2. how to power control them, either via creating ipmi service profile/applying the setting or directly via api call
3. how to tell the blade to pxe boot via api call
'''

def list_all_service_profiles(handle):
    '''
        This will list all the service profiles under org-root
        and print out :
          Name
          Dn ( absoulute location of the tree ) 
    '''
    rsp = handle.GetManagedObject(None, None,{"Dn":"org-root"})
    rsp = handle.GetManagedObject(rsp, "lsServer",{"Type":"instance"}, inHierarchical=False)
    
    for sp in rsp:
        print "Service Profile Name : [{}] , Dn : [{}]".format(sp.Name, sp.Dn)

def list_mac_address_of_all_service_profiles(handle, sp_name = None):
    #sp_name = 'a1c1b1_iscsi'
    handle.StartTransaction()
    rsp = handle.GetManagedObject(None, None,{"Dn":"org-root"})
    rsp = handle.GetManagedObject(rsp, "lsServer",{"Type":"instance","Name":sp_name}, inHierarchical=False)
    rsp = handle.GetManagedObject(rsp, "vnicEther",{}, inHierarchical=False)
    handle.CompleteTransaction()
    
    for vnic in rsp:
        print "Vnic Name : [{}] , Dn : [{}], Address : [{}]".format(vnic.Name, vnic.Dn, vnic.Addr )

        
def find_sp_by_mac(handle, mac_addr):
    # Single mac , query it directly 
    # if the mac_addr is a list , query the whole vnicEther , build a dictionary 
    handle.StartTransaction()
    rsp = handle.GetManagedObject(None, None,{"Dn":"org-root"})
    rsp = handle.GetManagedObject(rsp, "vnicEther",{'Addr': mac_addr}, inHierarchical=False)
    handle.CompleteTransaction()
    
    for vnic in rsp:
        print "Vnic Name : [{}] , Dn : [{}], Address : [{}]".format(vnic.Name, vnic.Dn, vnic.Addr )
    
if __name__ == "__main__":
    try :
        handle = UcsHandle()
        handle.Login("10.193.159.76","admin","Nbv12345")    
        list_all_service_profiles(handle)
        list_mac_address_of_all_service_profiles(handle)
    finally:
        handle.Logout()
