function RecoverFromVAE(h5file_path)
test_mesh = h5read(h5file_path,'/test_mesh');
gen=permute(test_mesh,[3,1,2]);
FLOGDR=gen(:,1:3,:);
FS=gen(:,4:9,:);
FLOGDR=reshape(FLOGDR,size(FLOGDR,1),size(FLOGDR,2)*size(FLOGDR,3));
FS=reshape(FS,size(FS,1),size(FS,2)*size(FS,3));
[ NLOGDR, NS ] = InverseMap(FLOGDR,FS);
for i = 1:size(NS,1)
    recon_noalign('ref.obj',['mesh',num2str(i),'.obj'],NLOGDR,NS);
end
